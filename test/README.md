# 文件内容智能分析程序

## 项目概述
本项目是一个智能化的文件分析工具，能够读取文件内容，将其转换为 JSON 格式，并利用本地 LLM（大语言模型）生成特定领域的深度分析报告及关键数据图表。程序会自动识别内容所属的专业领域（如金融、技术、医疗等），并提供生成的报告、数据和图表的下载链接。

## 环境要求
- **虚拟环境**: 使用现有的 `../.venv`。
- **LLM 支持**: 通过 MCP/Agent Skills 调用本地 LLM (Local LLM)。

## 系统架构

1.  **输入**: 文本类文件（如 txt, csv, log, md 等）。
2.  **核心处理**:
    *   **MCP Server**: 负责与底层文件系统交互（读写文件）及图表生成。
    *   **Agent (智能体)**: 负责流程编排与控制。
    *   **本地 LLM**:
        *   步骤 1: 将非结构化文本转换为结构化 JSON 数据。
        *   步骤 2: 识别内容的“专业领域”（Professional Domain）。
        *   步骤 3: 基于领域生成专业的 Markdown 分析报告。
        *   步骤 4: 提取关键数据点以供图表绘制。
3.  **输出结果**:
    *   JSON 数据文件 (`analysis_data.json`)。
    *   Markdown 分析报告 (`Analysis_Report_<Domain>.md`)。
    *   可视化图表 (PNG/SVG)。
    *   包含所有资源链接的汇总索引。

## 目录结构

*   `main.py`: 程序主入口。
*   `mcp_server.py`: MCP 服务器，提供文件读写和图表生成工具。
*   `agent.py`: 智能体逻辑，负责与 LLM 交互并调用 MCP 工具。
*   `utils.py`: 通用工具函数。
*   `*_analysis_output/`: 自动生成的分析结果输出目录。

## 使用方法

在终端中运行以下命令以分析指定文件：

```bash
# 请确保已激活虚拟环境
# source ../.venv/bin/activate

python test/main.py --input <文件路径>
```

**示例**:
```bash
python test/main.py --input test/sample_financial.txt
```

程序运行完成后，会在输入文件同级目录下生成一个名为 `<文件名>_analysis_output` 的文件夹，其中包含所有生成的分析产物。
