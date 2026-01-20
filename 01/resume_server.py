from fastmcp import FastMCP
import os

# 1. 初始化一个 MCP Server
# 就像给你的电脑开了一个名为 "Resume Tools" 的 USB 接口
mcp = FastMCP("Resume Tools")

# 2. 定义工具 (Tools)
# 使用装饰器 @mcp.tool，这会自动把函数转换成 LLM 能看懂的 Function Definition
@mcp.tool()
def list_resumes(directory: str) -> str:
    """
    列出指定文件夹下的所有简历文件。
    输入文件夹路径，返回文件名列表。
    """
    try:
        files = [f for f in os.listdir(directory) if f.endswith(('.txt', '.pdf', '.md'))]
        return f"找到以下简历: {', '.join(files)}"
    except Exception as e:
        return f"读取文件夹失败: {str(e)}"

@mcp.tool()
def read_resume_content(filepath: str) -> str:
    """
    读取单个简历文件的详细文本内容。
    输入完整文件路径，返回文本。
    """
    try:
        # 这里为了演示简单，假设是文本文件。实际项目可以用 pdfplumber 读取 PDF
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件内容失败: {str(e)}"

# 3. 运行服务
if __name__ == "__main__":
    mcp.run()