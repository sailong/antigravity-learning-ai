from fastmcp import FastMCP
import os
import json
import matplotlib.pyplot as plt
import utils

# Using the Agg backend for non-interactive plotting
plt.switch_backend('Agg')

# 配置 Matplotlib 以支持中文显示 (macOS)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

mcp = FastMCP("FileAnalysisServer")

@mcp.tool()
def generate_dashboard(output_dir: str, json_data: str, md_content: str, chart_files: str) -> str:
    """
    生成 HTML Dashboard 报告。
    """
    try:
        data = json.loads(json_data)
        charts = json.loads(chart_files)
        path = utils.generate_html_report(output_dir, data, md_content, charts)
        return f"Dashboard 生成成功: {path}"
    except Exception as e:
        return f"生成 Dashboard 失败: {str(e)}"

@mcp.tool()
def read_local_file(file_path: str) -> str:
    """读取本地文件内容。支持文本文件和 Excel (.xlsx, .xls)。"""
    if not os.path.exists(file_path):
        return f"错误: 文件未找到 {file_path}"
    
    try:
        _, ext = os.path.splitext(file_path)
        if ext.lower() in ['.xlsx', '.xls']:
            try:
                import pandas as pd
                # 读取所有 sheet
                xl = pd.read_excel(file_path, sheet_name=None)
                output = ""
                for sheet_name, df in xl.items():
                    output += f"### Sheet: {sheet_name}\n"
                    output += df.to_markdown(index=False)
                    output += "\n\n"
                return output
            except ImportError:
                return "错误: 未安装 pandas 或 openpyxl，无法读取 Excel 文件。"
            except Exception as e:
                return f"读取 Excel 文件时出错: {str(e)}"
        else:
            # 默认尝试作为文本读取
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        return f"读取文件时出错: {str(e)}"

@mcp.tool()
def save_file(file_path: str, content: str) -> str:
    """保存内容到本地文件。"""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"成功保存到 {file_path}"
    except Exception as e:
        return f"保存文件时出错: {str(e)}"

@mcp.tool()
def generate_chart(data_json: str, output_path: str, title: str = "Analysis Chart", chart_type: str = "bar") -> str:
    """
    从 JSON 数据生成图表。
    data_json 应为一个 JSON 字符串，表示包含 'label' 和 'value' 键的字典列表。
    """
    try:
        data = json.loads(data_json)
        if not data:
            return "错误: 未提供数据"
        
        labels = [str(item.get('label', 'Unknown')) for item in data]
        values = [float(item.get('value', 0)) for item in data]
        
        plt.figure(figsize=(10, 6))
        
        if chart_type == "pie":
            plt.pie(values, labels=labels, autopct='%1.1f%%')
        else:
            plt.bar(labels, values, color='skyblue')
            plt.xlabel('类别')
            plt.ylabel('数值')
        
        plt.title(title)
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        return f"图表已保存到 {output_path}"
    except Exception as e:
        return f"生成图表时出错: {str(e)}"

if __name__ == "__main__":
    mcp.run()
