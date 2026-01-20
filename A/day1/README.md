# Day 1: Python 与 LLM 的第一次握手

## 🎯 目标
编写一个 Python 脚本，让 AI 扮演“招聘经理”，无论用户问什么，它都只能用“严厉的面试官口吻”回答。

## 🛠️ 准备工作
我们需要一个能访问大模型的 Python 库。这里以最通用的 `openai` 库为例 (也适用于 DeepSeek, Moonshot 等支持 OpenAI 格式的模型)。

### 1. 安装库
在终端运行：
```bash
pip install openai
```

### 2. 获取 API Key
确保你有一个可用的 API Key。
- 如果是 OpenAI: `sk-...`
- 如果是 DeepSeek/其他: 同样是 `sk-...` 格式，并需要知道 `base_url`。

## 📝 核心概念
- **System Prompt (系统提示词)**: 设定 AI 的“人设”。例如：“你是一个面试官”。这是用户看不到的配置。
- **User Prompt (用户提示词)**: 用户的具体问题。例如：“你好，我来面试”。
- **Temperature (温度)**: 控制回答的随机性。面试官应该是严谨的 (数值较低, 如 0.3)。

## 🚀 开始编程
打开 `hiring_manager.py` 并按照注释填入你的 API 配置。
