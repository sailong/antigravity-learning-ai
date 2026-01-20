import asyncio
import os
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

# Configuration for Local LLM
LLM_API_BASE = "http://127.0.0.1:33333/v1"
LLM_API_KEY = "lm-studio"
MODEL_NAME = "local-model"

class AnalysisAgent:
    def __init__(self):
        self.client = AsyncOpenAI(base_url=LLM_API_BASE, api_key=LLM_API_KEY)
        self.python_executable = sys.executable
        # Assume mcp_server.py is in the same directory
        self.server_path = os.path.join(os.path.dirname(__file__), "mcp_server.py")

    async def analyze_file(self, file_path: str, output_dir: str):
        """
        编排分析流程:
        1. 通过 MCP 读取文件内容
        2. 通过 LLM 转换为 JSON
        3. 通过 LLM 确定领域
        4. 通过 LLM 生成报告
        5. 通过 MCP 生成图表
        6. 通过 MCP 保存报告
        """
        print(f"🚀 开始分析文件: {file_path}")
        
        # 连接到 MCP Server
        server_params = StdioServerParameters(command=self.python_executable, args=[self.server_path], env=os.environ.copy())
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # 1. 读取文件
                print("📖 正在读取文件内容...")
                read_result = await session.call_tool("read_local_file", arguments={"file_path": file_path})
                content = read_result.content[0].text
                
                if content.startswith("Error"):
                    print(f"❌ 读取文件失败: {content}")
                    return

                # 2. 分析内容 (JSON & 领域)
                print("🧠 正在使用本地 LLM 分析内容...")
                analysis_result = await self._analyze_content_with_llm(content)
                
                json_data = analysis_result.get("json_data", {})
                domain = analysis_result.get("domain", "General")
                report_md = analysis_result.get("report_markdown", "")
                chart_data = analysis_result.get("chart_data", [])
                
                # 3. 保存 JSON 数据
                json_filename = "analysis_data.json"
                json_path = os.path.join(output_dir, json_filename)
                print(f"💾 正在保存 JSON 数据到 {json_path}...")
                await session.call_tool("save_file", arguments={"file_path": json_path, "content": json.dumps(json_data, indent=2, ensure_ascii=False)})
                
                # 4. 生成图表
                chart_files = []
                if chart_data:
                    print("📊 正在生成图表...")
                    for i, data_point in enumerate(chart_data):
                        chart_filename = f"chart_{i+1}.png"
                        chart_path = os.path.join(output_dir, chart_filename)
                        title = data_point.get("title", "Chart")
                        points = data_point.get("data", [])
                        
                        if points:
                            await session.call_tool("generate_chart", arguments={
                                "data_json": json.dumps(points),
                                "output_path": chart_path,
                                "title": title
                            })
                            chart_files.append(chart_filename)
                
                # 5. 完成并保存报告
                print("📝 正在生成分析报告...")
                # 将下载链接附加到报告中
                report_md += "\n\n## 📂 生成文件清单 (下载链接)\n"
                report_md += f"- [数据文件 (JSON)](./{json_filename})\n"
                for cf in chart_files:
                    report_md += f"- [图表: {cf}](./{cf})\n"
                    # 在报告中嵌入图表
                    report_md = report_md.replace(f"<!-- CHART_{i+1} -->", f"![{cf}](./{cf})") # 基本占位符替换（如果有）

                report_filename = f"Analysis_Report_{domain}.md"
                report_path = os.path.join(output_dir, report_filename)
                await session.call_tool("save_file", arguments={"file_path": report_path, "content": report_md})
                
                print(f"✅ 分析完成! 报告已保存至 {report_path}")
                
                # 6. 生成 HTML Dashboard
                print("🌐 正在生成 HTML Dashboard...")
                await session.call_tool("generate_dashboard", arguments={
                    "output_dir": output_dir,
                    "json_data": json.dumps(json_data, ensure_ascii=False),
                    "md_content": report_md,
                    "chart_files": json.dumps(chart_files)
                })
                print(f"✨ 现代化 Dashboard 已生成: {os.path.join(output_dir, 'index.html')}")

    async def _analyze_content_with_llm(self, content: str) -> dict:
        """
        请求 LLM 执行:
        1. 识别领域
        2. 转换为 JSON
        3. 起草报告
        4. 提取图表数据
        """
        
        # 从文件加载系统提示词
        try:
            prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_prompt.md")
            with open(prompt_path, "r", encoding="utf-8") as f:
                core_system_prompt = f.read()
        except Exception as e:
            print(f"⚠️ 警告: 无法加载 system_prompt.md ({e}), 使用默认值。")
            core_system_prompt = "You are an intelligent data analyst. Please analyze the content provided."

        system_prompt = f"""
        {core_system_prompt}
        
        ---
        
        **OUTPUT INSTRUCTION**:
        输出一个有效的 JSON 对象，包含以下结构。
        所有字符串值（除键外）必须用简体中文。
        
        {{
            "domain": "专业领域 (例如，金融、医疗)",
            "json_data": {{ ...结构化数据... }},
            "report_markdown": "# 标题\\n\\n## Executive Summary\\n... (Markdown content in Chinese)",
            "chart_data": [
                {{
                    "title": "图表标题 (中文)",
                    "data": [ {{"label": "Label1 (In Chinese)", "value": 10}}, {{"label": "Label2", "value": 20}} ]
                }}
            ]
        }}
        
        IMPORTANT:
        1. 输出必须是有效的 JSON。
        2. 不要在字符串值中包含未转义的换行符。使用 \\n 代替。
        3. 不要输出 JSON 周围的 markdown 格式化（如 ```json ... ```）。只需原始 JSON。
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Here is the file content:\n\n{content[:4000]}"} 
                ],
                temperature=0.2
            )
            
            result_text = response.choices[0].message.content.strip()
            # Clean up potential markdown code blocks
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            elif result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result_text = result_text.strip()
            
            # Simple cleanup for common issues if not valid
            import re
            # Try to catch trailing commas before closing braces/brackets
            result_text = re.sub(r',(\s*[])}])', r'\1', result_text)
                
            return json.loads(result_text)
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback
            return {
                "domain": "Unknown",
                "json_data": {"raw": content[:500]},
                "report_markdown": f"# 分析失败\n\n错误信息: {str(e)}\n\n原始输出:\n{result_text[:1000] if 'result_text' in locals() else '无输出'}",
                "chart_data": []
            }

if __name__ == "__main__":
    # Test run
    agent = AnalysisAgent()
    # Mocking usage requires a file path
