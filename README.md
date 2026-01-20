# Antigravity（更新中）

Antigravity 是一个基于 Model Context Protocol (MCP) 的智能 Agent 学习与实验项目。本项目通过一系列循序渐进的课程（位于 `A/` 目录），引导开发者从零开始构建一个能够管理本地文件并进行智能分析的 AI Agent。

## 🛠 安装与环境配置

本项目依赖 Python 环境及相关的 AI 库。请按照以下步骤进行配置：

### 1. 准备 Python 环境

建议使用 Python 3.10 或更高版本。

#### 创建虚拟环境
在项目根目录下运行以下命令以保持依赖隔离：

```bash
python3 -m venv .venv
```

#### 激活虚拟环境
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

### 2. 安装依赖包

项目所需的依赖项已列在 `requirements.txt` 中。激活虚拟环境后，运行：

```bash
pip install -r requirements.txt
```

**核心依赖说明：**
- `mcp`: Model Context Protocol 官方库。
- `fastmcp`: 快速构建 MCP Server 的高层框架。
- `openai`: 用于与大模型（如 GPT-4）交互。
- `matplotlib` & `tabulate`: 用于结果的结构化展示与数据可视化。

### 3. 配置 API 密钥

你需要配置一个大模型的 API Key。建议在当前终端会话中设置环境变量，或者创建一个 `.env` 文件：

```bash
export OPENAI_API_KEY="your_api_key_here"
# 如果使用其他兼容 OpenAI 的模型（如 DeepSeek），可以设置：
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
```

#### 使用本地模型 (Ollama / LM Studio)

如果你希望在本地运行模型以保护隐私或节省成本，可以使用 Ollama 或 LM Studio。它们都提供兼容 OpenAI 的 API 接口：

- **Ollama**:
  1. 下载并安装 [Ollama](https://ollama.com/)。
  2. 运行模型：`ollama run llama3` (或你喜欢的任何模型)。
  3. 环境变量配置：
     ```bash
     export OPENAI_API_KEY="ollama" # 不能为空，可填任意字符串
     export OPENAI_BASE_URL="http://localhost:11434/v1"
     ```

- **LM Studio**:
  1. 下载并安装 [LM Studio](https://lmstudio.ai/)。
  2. 选择模型并开启 "Local Server"。
  3. 环境变量配置：
     ```bash
     export OPENAI_API_KEY="lm-studio"
     export OPENAI_BASE_URL="http://localhost:1234/v1"
     ```

   > 💡 **详细教程**：
   > - [LM Studio 本地部署 Qwen 指南](./LM_Studio_Qwen_Guide.md)
   > - [Antigravity 进阶使用技巧 16 则](./Antigravity_Usage_Tips.md)

---

## 🚀 快速开始

### 运行学习路线
项目核心教学内容位于 `A/README.md`。请按照其中的路线图进行学习：
- **Day 1-2**: 基础 API 调用与结构化输出。
- **Day 3-4**: 函数调用与 MCP Server 开发。
- **Day 5-6**: 构建 Agent Client 与思考循环。
- **Day 7-8**: 简历筛选实战项目。

### 运行示例代码
如果你已经完成了 Day 4 的任务，可以尝试启动 MCP Server：

```bash
# 示例：启动简历管理 MCP 服务
python A/day4/resume_server.py
```

---

## 📂 项目结构

- `A/`: 核心学习计划与每日练习代码。
- `requirements.txt`: 项目依赖列表。
- `.venv/`: Python 虚拟环境（用户本地创建）。

---

## 📝 许可证
MIT License
