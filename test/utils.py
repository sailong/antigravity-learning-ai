import json
import matplotlib.pyplot as plt
import os

# 配置 Matplotlib 以支持中文显示 (macOS)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def generate_chart(data: list, output_path: str, title: str = "Analysis Chart"):
    """
    从提供的数据生成图表并保存到 output_path。
    预期的数据格式: [{'label': 'A', 'value': 10}, ...]
    """
    if not data:
        return False
        
    labels = [item.get('label', 'Unknown') for item in data]
    values = [item.get('value', 0) for item in data]
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('类别')
    plt.ylabel('数值')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        return True
    except Exception as e:
        print(f"生成图表时出错: {e}")
        return False

def convert_to_json(data_str: str) -> dict:
    """尝试将字符串解析为 JSON。"""
    try:
        return json.loads(data_str)
    except json.JSONDecodeError:
        return {}

def generate_html_report(output_dir: str, json_data: dict, md_content: str, chart_files: list) -> str:
    """
    生成一个包含所有分析结果的现代 HTML 报告。
    """
    html_path = os.path.join(output_dir, "index.html")
    
    # 简单的 Markdown 到 HTML 转换 (为了不引入额外重依赖，这里使用了简单的替换，
    # 实际生产中建议在前端使用 marked.js)
    # 这里我们只做生成 HTML 结构，内容渲染交给前端 JS库
    
    json_str = json.dumps(json_data, ensure_ascii=False)
    charts_html = ""
    for chart in chart_files:
        charts_html += f'''
        <div class="bg-white p-4 rounded-lg shadow-md mb-6">
            <h3 class="text-lg font-semibold mb-2 text-gray-700">图表预览: {chart}</h3>
            <img src="./{chart}" alt="{chart}" class="w-full h-auto rounded-md border border-gray-100">
        </div>
        '''

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>项目分析报告 Dashboard</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Marked.js for Markdown rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; }}
        .markdown-body h1 {{ font-size: 2.25rem; font-weight: 700; margin-bottom: 1rem; color: #1f2937; }}
        .markdown-body h2 {{ font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }}
        .markdown-body h3 {{ font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #4b5563; }}
        .markdown-body p {{ margin-bottom: 1rem; line-height: 1.75; color: #4b5563; }}
        .markdown-body ul {{ list-style-type: disc; padding-left: 1.5rem; margin-bottom: 1rem; color: #4b5563; }}
        .markdown-body li {{ margin-bottom: 0.5rem; }}
        .markdown-body table {{ width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }}
        .markdown-body th, .markdown-body td {{ border: 1px solid #e5e7eb; padding: 0.75rem; text-align: left; }}
        .markdown-body th {{ background-color: #f9fafb; font-weight: 600; }}
        .markdown-body blockquote {{ border-left: 4px solid #3b82f6; padding-left: 1rem; font-style: italic; color: #6b7280; background-color: #eff6ff; padding: 1rem; border-radius: 0.25rem; }}
    </style>
</head>
<body class="text-gray-800">

    <div class="min-h-screen flex flex-col">
        <!-- Header -->
        <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                <div class="flex items-center">
                    <span class="text-2xl mr-2">📊</span>
                    <h1 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">智能分析 Dashboard</h1>
                </div>
                <div class="text-sm text-gray-500">生成时间: <span id="current-time"></span></div>
            </div>
        </header>

        <main class="flex-grow max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
            
            <!-- Main Content: Report -->
            <div class="space-y-8">
                <div class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100">
                    <div class="p-8">
                        <div id="report-content" class="markdown-body">
                            <!-- Markdown content will be rendered here -->
                        </div>
                    </div>
                </div>

                <!-- Inline Charts Section -->
                <div class="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
                    <h2 class="text-2xl font-bold text-gray-800 mb-6 border-l-4 border-blue-600 pl-4">📊 可视化图表分析</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {charts_html}
                    </div>
                    {f'<div class="text-gray-500 text-sm text-center py-4 italic">暂无图表生成</div>' if not chart_files else ''}
                </div>

                <!-- Attachments & Data (Moved from Sidebar) -->
                <div class="bg-gray-50 rounded-xl border border-gray-200 p-6">
                    <details class="group">
                        <summary class="flex justify-between items-center font-medium cursor-pointer list-none">
                            <span class="text-lg font-bold text-gray-700">📂 附件与原始数据</span>
                            <span class="transition group-open:rotate-180">
                                <svg fill="none" height="24" shape-rendering="geometricPrecision" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                            </span>
                        </summary>
                        <div class="text-neutral-600 mt-3 group-open:animate-fadeIn">
                            
                            <!-- Download Links -->
                            <div class="mb-6">
                                <h3 class="font-semibold mb-3 text-gray-600">资源下载</h3>
                                <ul class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <li>
                                        <a href="./analysis_data.json" download class="block bg-white border border-gray-200 hover:border-blue-500 hover:text-blue-600 transition px-4 py-2 rounded-lg text-sm flex items-center justify-between">
                                            <span>📄 JSON 数据</span>
                                            <span>↓</span>
                                        </a>
                                    </li>
                                    { ''.join([f'''
                                    <li>
                                        <a href="./{chart}" download class="block bg-white border border-gray-200 hover:border-blue-500 hover:text-blue-600 transition px-4 py-2 rounded-lg text-sm flex items-center justify-between">
                                            <span>📊 {chart}</span>
                                            <span>↓</span>
                                        </a>
                                    </li>''' for chart in chart_files]) }
                                </ul>
                            </div>

                            <!-- JSON Preview -->
                            <div>
                                <h3 class="font-semibold mb-3 text-gray-600">JSON 数据预览</h3>
                                <div class="bg-gray-800 rounded-lg p-4 overflow-auto max-h-60 text-xs font-mono text-green-400 border border-gray-700">
                                    <pre id="json-viewer"></pre>
                                </div>
                            </div>

                        </div>
                    </details>
                </div>
            </div>

        </main>
'''

        <footer class="bg-white border-t border-gray-200 mt-auto">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <p class="text-center text-sm text-gray-400">
                    Generated by Antigravity AI Analysis Agent
                </p>
            </div>
        </footer>
    </div>

    <script>
        // Data Injection
        const mdContent = {json.dumps(md_content)};
        const jsonData = {json_str};

        // Render Markdown
        document.getElementById('report-content').innerHTML = marked.parse(mdContent);

        // Render JSON Preview (Pretty Print)
        document.getElementById('json-viewer').textContent = JSON.stringify(jsonData, null, 2);

        // Set Time
        document.getElementById('current-time').textContent = new Date().toLocaleString('zh-CN');
    </script>
</body>
</html>
    """
    
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return html_path
    except Exception as e:
        print(f"Error generating HTML: {e}")
        return ""
