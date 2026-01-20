import asyncio
import os
import json
import sys
from openai import OpenAI

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. 系统指令：明确 Agent 的职责和输出格式
SYSTEM_PROMPT = """
你是一个专业的招聘筛选专家。你的任务是读取候选人简历，提取关键信息，并根据要求进行筛选打分。

# 你的工作流程
1. 使用 `list_resumes` 工具查看 `resumes` 目录下的所有简历文件。
2. 使用 `read_resume_content` 工具读取简历内容。由于上下文限制，你可以**只读取前 3-5 份**包含 "Python" 或 "Tech" 关键词的简历进行演示。
3. 分析简历内容，提取：姓名、技能、工作年限、匹配度评分。
4. 最终输出一个 JSON 列表。

# 核心规则
- 你必须返回 JSON 格式的数据。
- 不要返回 Markdown 格式（如 ```json），直接返回纯 JSON 字符串。
- 评分标准：Python/Go/Java (+20), 3年以上经验 (+20), 本科 (+10).

# 最终输出示例
[
    {
        "filename": "Tech_Python_张三.txt",
        "name": "张三",
        "score": 85,
        "skills": ["Python", "Django"],
        "reason": "经验丰富，技术栈匹配"
    }
]
"""

# 2. 配置 LLM 客户端
client = OpenAI(
    base_url="http://127.0.0.1:33333/v1", 
    api_key="lm-studio"
)

# 3. 工具格式转换 (MCP -> OpenAI)
def format_mcp_tools_for_openai(mcp_tools):
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })
    return openai_tools

# 4. Agent 核心思考循环
async def agent_loop(session, tools, user_query):
    # 初始化对话历史
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    openai_tools = format_mcp_tools_for_openai(tools)
    max_turns = 15 # 防止死循环
    
    print(f"\n🧠 Agent 收到任务: {user_query}")

    for turn in range(max_turns):
        print(f"\n🔄 [第 {turn + 1} 回合] 思考中...")
        
        # A. 调用 LLM
        try:
            response = client.chat.completions.create(
                model="qwen3-8b", 
                messages=messages,
                tools=openai_tools,
                temperature=0.1, 
            )
        except Exception as e:
            print(f"❌ LLM 调用失败: {e}")
            return None

        message = response.choices[0].message
        content = message.content
        tool_calls = message.tool_calls

        # 将 LLM 的回复加入历史（非常重要，否则下一轮会报错）
        messages.append(message)

        # B. 情况 1: LLM 请求调用工具
        if tool_calls:
            print(f"�️  Agent 决定调用工具: {[t.function.name for t in tool_calls]}")
            
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_args_str = tool_call.function.arguments
                call_id = tool_call.id
                
                try:
                    func_args = json.loads(func_args_str)
                except json.JSONDecodeError:
                    print(f"⚠️ 参数解析错误: {func_args_str}")
                    func_args = {}

                print(f"   ➤ 执行: {func_name}({func_args})")
                
                # --- 真正的 MCP 调用 ---
                try:
                    # session.call_tool 返回的是 CallToolResult 对象
                    mcp_result = await session.call_tool(func_name, arguments=func_args)
                    
                    # 提取文本内容
                    tool_output_text = ""
                    if mcp_result.content:
                        for content_item in mcp_result.content:
                            if content_item.type == "text":
                                tool_output_text += content_item.text
                    
                    # 截断过长的输出，节省 token
                    if len(tool_output_text) > 2000:
                        tool_output_text = tool_output_text[:2000] + "...(内容过长已截断)"
                    
                    print(f"   ✅ 结果: {tool_output_text[:100]}...")

                except Exception as e:
                    tool_output_text = f"Error executing tool: {str(e)}"
                    print(f"   ❌ 工具执行出错: {e}")

                # 将工具执行结果作为 'tool' 角色消息返回给 LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": tool_output_text
                })
            
            # 工具执行完，直接进入下一轮循环，让 LLM 看到结果并继续思考
            continue

        # C. 情况 2: LLM 没有调用工具，可能是输出了最终结果
        if content:
            # 尝试解析 JSON
            cleaned_content = content.replace("```json", "").replace("```", "").strip()
            # 尝试简单清洗开头结尾
            if cleaned_content.startswith("json"):
                 cleaned_content = cleaned_content[4:].strip()

            try:
                data = json.loads(cleaned_content)
                print("\n✨ JSON 解析成功！")
                return data # 成功结束
            except json.JSONDecodeError:
                # 只有当看起来像是由于格式错误导致解析失败时才重试
                if "[" in cleaned_content or "{" in cleaned_content:
                     print(f"⚠️ JSON 解析失败，尝试让 Agent 修复...")
                     error_msg = "你的回复无法解析为标准的 JSON。请不要输出 Markdown，只输出 JSON 内容 (例如 [...])。"
                     messages.append({"role": "user", "content": error_msg})
                else:
                    # 可能是普通的对话回复，不是 JSON
                    print(f"🤖 Agent: {content}")
                    # 自动提示它：请开始执行或输出 JSON
                    # messages.append({"role": "user", "content": "请继续..."})
                    pass
    
    print("❌ 超过最大迭代次数，任务未完成。")
    return None

async def run_smart_agent():
    # 1. 启动 MCP Server
    server_params = StdioServerParameters(
        command=sys.executable, 
        args=["resume_server.py"], 
        env=os.environ.copy()
    )

    print(f"🔌 正在启动 MCP Server ({sys.executable})...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 获取工具
            tools = await session.list_tools()
            print(f"🔧 激活工具: {[t.name for t in tools.tools]}")
            
            # 开始任务
            # 注意：我在 Prompt 里指定了去 resumes 目录找
            final_json = await agent_loop(session, tools.tools, "请筛选 resumes 目录下的简历，找出适合做 Python 开发的候选人。")
            
            if final_json:
                print("\n================ 最终结果 ================")
                print(json.dumps(final_json, indent=4, ensure_ascii=False))
                print("==========================================")
                
                # 可选：保存到文件
                with open("filtered_resumes.json", "w", encoding="utf-8") as f:
                     json.dump(final_json, f, indent=4, ensure_ascii=False)
                print("已保存到 filtered_resumes.json")

if __name__ == "__main__":
    asyncio.run(run_smart_agent())