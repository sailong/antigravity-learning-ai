import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 这是我们的“大脑”逻辑（暂时由代码写死，下一步接入 LLM）
async def run_agent_process():
    # 1. 定义如何启动 Server
    # 我们告诉 Client："去运行 python resume_server.py 这个命令来启动服务"
    server_params = StdioServerParameters(
        command="python",  # 如果你的环境是 python3，请修改这里
        args=["resume_server.py"], 
        env=os.environ.copy() # 继承当前环境变量
    )

    print("🔌 正在连接 MCP Server...")

    # 2. 建立 Stdio 连接通道
    async with stdio_client(server_params) as (read, write):
        # 3. 创建会话 (Session)
        async with ClientSession(read, write) as session:
            # 初始化握手
            await session.initialize()
            
            # --- 阶段 1: 感知能力 ---
            # Agent 第一步是看看自己有了什么新“手”
            tools = await session.list_tools()
            print(f"\n✅ 连接成功! 发现工具: {[t.name for t in tools.tools]}")
            
            # --- 阶段 2: 执行筛选任务 (模拟 Agent 思考过程) ---
            
            # 步骤 A: Agent 决定先看看有哪些简历
            print("\n🤖 Agent 思考: '我需要先获取简历列表...'")
            # 真正调用 list_resumes 工具
            result_list = await session.call_tool("list_resumes", arguments={"directory": "./resumes"})
            files_text = result_list.content[0].text
            print(f"📄 工具返回结果: {files_text}")

            # 步骤 B: Agent 决定读取其中一个文件
            # (这里我们为了演示，手动解析一下结果，假设我们要读 agent_client.py 自己)
            target_file = "agent_client.py" 
            
            print(f"\n🤖 Agent 思考: '我要读取 {target_file} 的内容进行分析...'")
            result_content = await session.call_tool("read_resume_content", arguments={"filepath": target_file})
            
            # 打印文件内容的前 100 个字符
            content_preview = result_content.content[0].text[:100]
            print(f"📖 工具返回内容 (预览):\n{content_preview}...")
            
            print("\n✨ 任务完成：Agent 成功调用了外部工具获取了数据！")

if __name__ == "__main__":
    # 运行异步主程序
    asyncio.run(run_agent_process())