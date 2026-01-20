# Day 3 巩固练习

## 📚 核心知识点回顾

### 1. 什么是 Function Calling?

**简单理解:**
Function Calling 就是让 AI 能够"使用工具"。AI 本身只是一个"大脑",通过 Function Calling,我们给它装上了"手脚"。

**类比:**
- **没有 Function Calling**: AI 像一个只会说话的人,你问"今天天气怎么样?",它只能说"抱歉,我不知道"
- **有了 Function Calling**: AI 像一个有手机的人,它会说"让我查一下",然后调用 `get_weather()` 函数获取实时数据

---

## 🎯 核心概念详解

### 概念 1: Tools Definition (工具定义)

**作用:** 告诉 AI 有哪些工具可以使用,以及如何使用它们。

**结构:**
```python
tools = [
    {
        "type": "function",           # 工具类型
        "function": {
            "name": "函数名",          # 函数的唯一标识
            "description": "函数描述",  # 告诉 AI 这个函数是干什么的
            "parameters": {            # 函数需要什么参数
                "type": "object",
                "properties": {
                    "参数名": {
                        "type": "参数类型",
                        "description": "参数说明"
                    }
                },
                "required": ["必需参数列表"]
            }
        }
    }
]
```

**示例:**
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息,包括温度、天气状况和湿度",
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
}]
```

**关键点:**
- `description` 要清晰明确,AI 根据这个判断是否调用
- `parameters` 使用 JSON Schema 格式
- `required` 指定哪些参数是必需的

---

### 概念 2: Tool Choice (工具选择)

**作用:** 控制 AI 是否/如何调用函数。

**选项:**

| 值 | 含义 | 使用场景 |
|---|------|----------|
| `"auto"` | AI 自动决定是否调用 | 最常用,让 AI 智能判断 |
| `"none"` | 不允许调用任何函数 | 只想要普通对话 |
| `"required"` | 强制 AI 必须调用函数 | 确保 AI 使用工具 |
| `{"type": "function", "function": {"name": "xxx"}}` | 强制调用指定函数 | 明确知道要调用哪个 |

**示例:**
```python
# 让 AI 自动决定
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    tools=tools,
    tool_choice="auto"  # 推荐
)
```

---

### 概念 3: Tool Calls (函数调用请求)

**作用:** AI 返回的函数调用指令。

**结构:**
```python
assistant_message.tool_calls = [
    {
        "id": "call_abc123",              # 调用 ID (用于追踪)
        "type": "function",               # 类型
        "function": {
            "name": "get_weather",        # 要调用的函数名
            "arguments": '{"city": "北京"}'  # 参数 (JSON 字符串!)
        }
    }
]
```

**关键点:**
- `arguments` 是 **JSON 字符串**,需要用 `json.loads()` 解析
- 一次可能有多个 `tool_calls` (AI 可能同时调用多个函数)
- `id` 用于将函数结果关联回对应的调用

---

### 概念 4: 多轮对话流程

**完整流程:**

```
第 1 轮: 用户提问
   ↓
   AI 分析并决定调用函数
   ↓
   返回 tool_calls
   
第 2 轮: 执行函数
   ↓
   将结果以 "tool" 角色加入对话
   ↓
   再次调用 AI
   ↓
   AI 根据函数结果生成最终回复
```

**代码实现:**
```python
# 第 1 轮
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    tools=tools
)

if response.choices[0].message.tool_calls:
    # 有函数调用
    messages.append(response.choices[0].message)
    
    # 执行函数
    for tool_call in response.choices[0].message.tool_calls:
        result = execute_function(tool_call)
        
        # 将结果加入对话
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": result
        })
    
    # 第 2 轮
    final_response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )
```

---

## 🔍 常见问题解答

### Q1: 为什么 AI 不直接执行函数?

**A:** 安全性和控制权!

如果 AI 能直接执行代码:
- ❌ AI 可能删除文件
- ❌ AI 可能访问敏感数据
- ❌ AI 可能进行危险操作

通过让你的代码执行函数:
- ✅ 你可以验证参数
- ✅ 你可以添加权限检查
- ✅ 你可以记录所有操作

---

### Q2: arguments 为什么是字符串?

**A:** 为了兼容性和灵活性。

```python
# AI 返回的是字符串
arguments = '{"city": "北京", "date": "2024-01-01"}'

# 你需要解析
args = json.loads(arguments)
city = args["city"]  # "北京"
```

---

### Q3: 如果 AI 调用了不存在的函数怎么办?

**A:** 添加错误处理!

```python
function_name = tool_call.function.name

if function_name in AVAILABLE_FUNCTIONS:
    result = AVAILABLE_FUNCTIONS[function_name](**args)
else:
    result = json.dumps({
        "error": f"函数 {function_name} 不存在"
    })
```

---

### Q4: 可以一次调用多个函数吗?

**A:** 可以! AI 可能返回多个 `tool_calls`。

```python
for tool_call in assistant_message.tool_calls:
    # 依次执行每个函数调用
    result = execute_function(tool_call)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })
```

---

## 💡 实战技巧

### 技巧 1: 写好函数描述

❌ **糟糕的描述:**
```python
"description": "查天气"
```

✅ **优秀的描述:**
```python
"description": "获取指定城市的实时天气信息,包括天气状况、温度、湿度等详细数据。支持中国主要城市。"
```

**原则:**
- 说明函数的**具体功能**
- 说明**返回什么数据**
- 说明**限制条件** (如支持哪些城市)

---

### 技巧 2: 参数验证

```python
def get_weather(city):
    # 验证参数
    if not city:
        return json.dumps({"error": "城市名称不能为空"})
    
    if city not in SUPPORTED_CITIES:
        return json.dumps({"error": f"不支持城市: {city}"})
    
    # 执行逻辑
    ...
```

---

### 技巧 3: 统一返回格式

**建议:** 函数始终返回 JSON 字符串

```python
def get_weather(city):
    # 成功
    return json.dumps({
        "status": "success",
        "data": {"weather": "晴天", "temperature": "15°C"}
    }, ensure_ascii=False)
    
    # 失败
    return json.dumps({
        "status": "error",
        "message": "城市不存在"
    }, ensure_ascii=False)
```

---

### 技巧 4: 调试技巧

**打印关键信息:**
```python
print(f"📞 调用函数: {function_name}")
print(f"📋 参数: {arguments}")
print(f"⚙️  结果: {result}")
```

**检查 tool_calls:**
```python
if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
    print(f"发现 {len(assistant_message.tool_calls)} 个函数调用")
else:
    print("AI 没有调用函数")
```

---

## 🚀 挑战练习

### 练习 A: 添加新函数

在 `function_calling_demo.py` 中添加一个新函数:

```python
def get_time(timezone="Asia/Shanghai"):
    """获取指定时区的当前时间"""
    from datetime import datetime
    import pytz
    
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return json.dumps({
        "timezone": timezone,
        "time": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }, ensure_ascii=False)
```

**任务:**
1. 将函数添加到 `AVAILABLE_FUNCTIONS`
2. 添加对应的 tool definition
3. 测试: "现在几点了?"

---

### 练习 B: 处理错误

修改 `calculate` 函数,添加更严格的安全检查:

```python
def calculate(expression):
    # 1. 检查长度
    if len(expression) > 100:
        return json.dumps({"error": "表达式太长"})
    
    # 2. 检查危险字符
    dangerous = ["import", "eval", "exec", "__"]
    if any(d in expression for d in dangerous):
        return json.dumps({"error": "表达式包含危险内容"})
    
    # 3. 执行计算
    ...
```

---

### 练习 C: 多函数调用

创建一个场景,让 AI 同时调用多个函数:

**用户问题:** "北京和上海哪个城市温度更高?"

**期望流程:**
1. AI 调用 `get_weather("北京")`
2. AI 调用 `get_weather("上海")`
3. AI 比较两个结果
4. AI 生成回复

---

## ✅ 自检清单

完成以下检查,确保你真正掌握了 Day 3:

- [ ] 我能解释 Function Calling 的作用
- [ ] 我理解 Tools Definition 的结构
- [ ] 我知道 tool_choice 的不同选项
- [ ] 我理解为什么 arguments 是字符串
- [ ] 我能写出完整的多轮对话流程
- [ ] 我知道如何处理函数执行错误
- [ ] 我能添加新的函数到系统中
- [ ] 我理解为什么 AI 不直接执行函数

---

## 📖 延伸阅读

### Function Calling 的应用场景

1. **智能客服**: 查询订单、修改信息
2. **数据分析**: 查询数据库、生成报表
3. **自动化工具**: 发送邮件、创建任务
4. **智能家居**: 控制设备、查询状态

### 最佳实践

1. **函数要单一职责** - 一个函数只做一件事
2. **参数要明确** - 避免模糊的参数名
3. **返回要一致** - 统一使用 JSON 格式
4. **错误要友好** - 返回清晰的错误信息

---

## 🎓 知识点对比

### Day 2 vs Day 3

| 维度 | Day 2 (JSON 输出) | Day 3 (Function Calling) |
|------|-------------------|--------------------------|
| **目的** | 让 AI 输出结构化数据 | 让 AI 执行操作 |
| **交互** | 1 轮对话 | 2+ 轮对话 |
| **AI 角色** | 数据提取器 | 任务规划器 |
| **你的角色** | 解析 JSON | 执行函数 |
| **应用** | 信息提取 | 智能助手 |

---

全部理解后,你就可以继续 Day 4 了! 🎉
