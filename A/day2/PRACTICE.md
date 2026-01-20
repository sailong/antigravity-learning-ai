# Day 2 巩固练习

## 📚 核心知识点回顾

### 1. 为什么需要结构化输出?

**场景对比:**

❌ **没有结构化输出时:**
```
AI: "这位候选人叫张伟,他会Python、Java等技术,工作了大概3年左右..."
```
你需要写复杂的代码来解析这段文字,提取姓名、技能、年限等信息。

✅ **有结构化输出时:**
```json
{
  "name": "张伟",
  "skills": ["Python", "Java"],
  "experience_years": 3
}
```
直接用 `data["name"]` 就能获取信息!

---

## 🎯 练习 1: 理解 JSON 格式

### JSON 基础语法

```json
{
  "字符串": "值",
  "数字": 123,
  "布尔值": true,
  "空值": null,
  "数组": ["item1", "item2", "item3"],
  "对象": {
    "嵌套字段": "嵌套值"
  }
}
```

### Python 中的对应关系

| JSON 类型 | Python 类型 | 示例 |
|-----------|-------------|------|
| `{}` | `dict` | `{"name": "张三"}` |
| `[]` | `list` | `["Python", "Java"]` |
| `"string"` | `str` | `"张三"` |
| `123` | `int/float` | `3` |
| `true/false` | `bool` | `True/False` |
| `null` | `None` | `None` |

### 动手试试:

```python
import json

# JSON 字符串 -> Python 对象
json_str = '{"name": "张三", "age": 25, "skills": ["Python", "Java"]}'
data = json.loads(json_str)

print(data["name"])        # 输出: 张三
print(data["skills"][0])   # 输出: Python
print(type(data))          # 输出: <class 'dict'>

# Python 对象 -> JSON 字符串
person = {
    "name": "李四",
    "age": 30,
    "skills": ["JavaScript", "React"]
}
json_output = json.dumps(person, ensure_ascii=False, indent=2)
print(json_output)
```

---

## 🎯 练习 2: Prompt Engineering 的威力

### 对比不同的 System Prompt

**❌ 糟糕的 Prompt:**
```python
system_prompt = "帮我提取简历信息"
```
AI 可能回复: "好的,我看到这位候选人叫张伟,他会Python..."

**✅ 优秀的 Prompt:**
```python
system_prompt = """你是信息提取助手。
只输出 JSON 格式,不要任何解释。
格式: {"name": "姓名", "skills": ["技能1", "技能2"]}"""
```
AI 会直接输出: `{"name": "张伟", "skills": ["Python", "Java"]}`

### 关键要素:

1. **明确角色**: "你是信息提取助手"
2. **明确格式**: "只输出 JSON"
3. **提供示例**: 给出具体的 JSON 格式
4. **禁止废话**: "不要任何解释"

---

## 🎯 练习 3: 处理 AI 的"不听话"

### 问题: AI 有时会输出额外内容

```
好的,我帮你整理了:
{"name": "张伟", "skills": ["Python"]}
希望对你有帮助!
```

### 解决方案: 正则表达式提取

```python
import re
import json

def extract_json(text):
    # 匹配 JSON 对象 (大括号包裹的内容)
    pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except:
            continue
    return None

# 测试
messy_text = """好的,我帮你整理了:
{"name": "张伟", "skills": ["Python", "Java"]}
希望对你有帮助!"""

result = extract_json(messy_text)
print(result)  # 输出: {'name': '张伟', 'skills': ['Python', 'Java']}
```

---

## 🎯 练习 4: Temperature 参数的影响

### Temperature 是什么?

控制 AI 输出的**随机性**:
- `0.0`: 完全确定,每次输出相同
- `0.3`: 较为确定,适合结构化输出
- `0.7`: 较为灵活,适合创意对话
- `1.0`: 非常随机,适合创作

### 实验对比:

```python
# Temperature = 0.3 (推荐用于 JSON 输出)
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=0.3  # 输出更稳定
)

# Temperature = 0.7 (适合对话)
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=0.7  # 输出更灵活
)
```

---

## 💡 实战建议

### 1. 调试技巧

在 `resume_parser.py` 中,我们打印了 AI 的原始回复:
```python
print(f"\n📄 AI 原始回复:\n{ai_reply}\n")
```
这样可以看到 AI 是否真的按要求输出了 JSON。

### 2. 错误处理

总是用 `try-except` 包裹 JSON 解析:
```python
try:
    data = json.loads(ai_reply)
except json.JSONDecodeError as e:
    print(f"JSON 解析失败: {e}")
    # 尝试用正则表达式提取
```

### 3. 数据验证

解析成功后,验证数据是否符合预期:
```python
if "name" not in data or "skills" not in data:
    print("警告: 缺少必要字段")

if not isinstance(data["skills"], list):
    print("警告: skills 应该是数组")
```

---

## 🚀 挑战练习

### 练习 A: 修改字段

修改 `resume_parser.py`,添加以下字段:
- `phone`: 电话号码
- `email`: 邮箱
- `github`: GitHub 链接

### 练习 B: 批量处理

创建一个新脚本,能够:
1. 读取多个自我介绍 (从文件或列表)
2. 批量调用 AI 提取信息
3. 将结果保存为 JSON 文件

### 练习 C: 数据分析

基于提取的 JSON 数据:
1. 统计最常见的技能
2. 计算平均工作年限
3. 按工作年限排序候选人

---

## 📖 延伸阅读

### JSON 相关
- [JSON 官方文档](https://www.json.org/json-zh.html)
- Python `json` 模块文档

### Prompt Engineering
- 明确性 > 模糊性
- 示例 > 描述
- 约束 > 自由

### 正则表达式
- `r'\{.*?\}'`: 匹配 JSON 对象
- `re.DOTALL`: 让 `.` 匹配换行符

---

## ✅ 自检清单

完成以下检查,确保你真正掌握了 Day 2:

- [ ] 我能解释为什么需要结构化输出
- [ ] 我理解 JSON 的基本语法
- [ ] 我知道如何用 `json.loads()` 和 `json.dumps()`
- [ ] 我能写出强制 AI 输出 JSON 的 System Prompt
- [ ] 我理解 Temperature 参数的作用
- [ ] 我能用正则表达式从文本中提取 JSON
- [ ] 我能处理 JSON 解析失败的情况

全部打勾后,你就可以继续 Day 3 了! 🎉
