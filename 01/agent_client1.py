import asyncio
import os
# 假设我们使用一个通用的 LLM 库 (这里用伪代码表示核心逻辑，方便你理解流程)
# from openai import OpenAI 

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 这是你的系统指令，赋予 Agent 角色
# SYSTEM_PROMPT = """
# 你是一个专业的招聘经理。
# 你的目标是筛选简历。
# 请使用提供的工具来读取文件列表和内容。
# 最后输出一个评分表格。
# """
SYSTEM_PROMPT = """
你是一个专业的招聘筛选专家。你的任务是提取简历的关键信息并打分。

# 核心规则
1. 你必须严格按照 JSON 格式输出，不要包含任何其他废话。
2. 每次分析完一份简历，只输出该简历的结构化数据。

# 评分标准 (0-100分)
- 关键词匹配: Python, MCP, Agent (每个+20分)
- 经验: 3年以上 (+20分)
- 学历: 本科及以上 (+20分)

# 输出格式示例
{
    "name": "候选人姓名",
    "score": 85,
    "skills": ["Python", "MCP"],
    "summary": "简短评价..."
}
"""

async def run_smart_agent():
    # 1. 启动 MCP Server (和之前一样)
    server_params = StdioServerParameters(
        command="python", 
        args=["resume_server.py"], 
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 2. 获取工具 (Hands)
            tools = await session.list_tools()
            print(f"🔧 激活工具: {[t.name for t in tools.tools]}")

            # 3. 初始用户任务
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "帮我筛选一下当前文件夹里的简历，我要找懂 Python 的人。"}
            ]

            # --- 核心循环 (The Loop) ---
            print("\n🧠 Agent 开始思考...")
            
            # 这里是一个简化的循环逻辑
            while True:
                # A. 调用 LLM (Brain)
                # response = client.chat.completions.create(model="gpt-4", messages=messages, tools=convert_to_openai_tools(tools))
                
                # 假设 LLM 返回了： "请调用 list_resumes()" 
                # (这里我们模拟 LLM 的第一次决策)
                print("🤖 LLM 决定: 调用 list_resumes 工具")
                
                # B. 执行工具 (Action)
                # 真正的 MCP 调用发生在这里！
                tool_name = "list_resumes"
                tool_args = {"directory": "."}
                
                result = await session.call_tool(tool_name, arguments=tool_args)
                tool_output = result.content[0].text
                print(f"📄 MCP Server 反馈: {tool_output}")

                # C. 将结果写回历史记录 (Memory)
                messages.append({
                    "role": "function", 
                    "name": tool_name, 
                    "content": tool_output
                })

                # D. 再次询问 LLM
                # LLM 看到文件列表后，会发起第二次调用："读取 resume_1.txt"
                # ... 循环直到 LLM 说 "完成"
                
                print("✨ (模拟结束) Agent 拿到文件列表后，下一步就会自动请求读取内容了。")
                break 

if __name__ == "__main__":
    asyncio.run(run_smart_agent())