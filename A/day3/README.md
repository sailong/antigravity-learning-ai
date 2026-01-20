# Day 3: 给 AI 装上"假肢" (Function Calling)

## 🎯 目标
理解 **Function Calling (函数调用)** 的原理,让 AI 不仅会"说",还会"做"!

写一个伪代码 Agent:用户问"今天天气",AI 返回 `{call: get_weather}`,你手动打印出"天气很好"。

## 🤔 为什么需要 Function Calling?

### Day 1-2 的局限性

到目前为止,AI 只能:
- ✅ 对话交流 (Day 1)
- ✅ 输出结构化数据 (Day 2)

但 AI **不能**:
- ❌ 查询数据库
- ❌ 读取文件
- ❌ 调用 API
- ❌ 执行计算

**问题场景:**
```
用户: "帮我查一下今天的天气"
AI: "抱歉,我无法访问实时天气数据..."
```

AI 只是一个"大脑",它需要"手脚"来与外部世界交互!

---

## 💡 Function Calling 的核心思想

### 流程图

```
用户提问
   ↓
AI 分析问题
   ↓
AI 决定: "我需要调用 get_weather 函数"
   ↓
AI 返回: {"function": "get_weather", "arguments": {"city": "北京"}}
   ↓
你的代码执行: result = get_weather("北京")
   ↓
将结果返回给 AI
   ↓
AI 生成最终回复: "北京今天晴天,温度 15°C"
```

### 关键点

1. **AI 不直接执行函数** - 它只是"建议"调用哪个函数
2. **你的代码负责执行** - 保证安全性和控制权
3. **结果返回给 AI** - AI 根据结果生成用户友好的回复

---

## 📝 核心概念

### 1. Function Definition (工具描述)

告诉 AI 有哪些"工具"可用:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称,例如: 北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
```

### 2. Function Call (函数调用请求)

AI 的回复中会包含:

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"city\": \"北京\"}"
      }
    }
  ]
}
```

### 3. Function Result (函数结果)

你执行函数后,将结果返回给 AI:

```python
messages.append({
    "role": "tool",
    "tool_call_id": "call_123",
    "content": "北京今天晴天,温度 15°C"
})
```

---

## 🚀 今天的任务

### 阶段 1: 理解原理 (伪代码)

创建一个简单的示例,**手动模拟** Function Calling 流程:

```python
# 用户问题
user_question = "今天天气怎么样?"

# AI 分析后决定调用函数
ai_decision = {
    "function": "get_weather",
    "arguments": {"city": "北京"}
}

# 你手动执行函数
def get_weather(city):
    return f"{city}今天天气很好!"

result = get_weather(ai_decision["arguments"]["city"])
print(result)  # 输出: 北京今天天气很好!
```

### 阶段 2: 真实实现

使用 OpenAI 的 Function Calling API,让 AI 真正调用函数。

---

## 🔑 关键挑战

### 挑战 1: 定义清晰的函数描述

❌ **糟糕的描述:**
```python
"description": "获取天气"
```

✅ **优秀的描述:**
```python
"description": "获取指定城市的实时天气信息,包括温度、天气状况等"
```

### 挑战 2: 处理参数解析

AI 返回的 `arguments` 是 **JSON 字符串**,需要解析:

```python
import json
args_str = '{"city": "北京"}'
args = json.loads(args_str)
city = args["city"]
```

### 挑战 3: 多轮对话

Function Calling 需要**至少两轮对话**:
1. 第一轮: AI 决定调用函数
2. 第二轮: 将函数结果返回给 AI,生成最终回复

---

## 📖 实战示例

我们将创建一个简单的 Agent,支持两个函数:
1. `get_weather(city)` - 获取天气 (模拟数据)
2. `calculate(expression)` - 计算数学表达式

用户可以问:
- "北京今天天气怎么样?"
- "帮我算一下 123 * 456"

---

## 💡 学习建议

1. **先理解流程** - 不要急着写代码,先画出流程图
2. **从简单开始** - 先用伪代码模拟,再用真实 API
3. **打印调试信息** - 每一步都打印出来,看清楚数据流动

---

现在打开 `function_calling_demo.py` 开始编程!
