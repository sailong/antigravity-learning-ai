# Day 2: 结构化输出 (JSON)

## 🎯 目标
修改 Day 1 的脚本,让 AI 帮你把一段乱七八糟的自我介绍,整理成结构化的 JSON 格式:
```json
{
  "name": "张三",
  "skills": ["Python", "机器学习"],
  "experience_years": 3
}
```

## 🤔 为什么需要结构化输出?

在 Day 1 中,我们让 AI 扮演面试官,它的回复是**自然语言文本**。但在实际应用中,我们经常需要:
- 从 AI 的回复中**提取关键信息**
- 将信息**存入数据库**
- 进行**数据分析和排序**

如果 AI 只会"废话连篇",我们就需要写复杂的正则表达式来解析。但如果 AI 直接输出 JSON,一切都变简单了!

## 📝 核心概念

### 1. JSON 格式
JSON (JavaScript Object Notation) 是一种轻量级的数据交换格式:
```json
{
  "key1": "value1",
  "key2": 123,
  "key3": ["item1", "item2"],
  "key4": {
    "nested_key": "nested_value"
  }
}
```

### 2. Prompt Engineering (提示词工程)
通过精心设计的提示词,**强制** AI 输出特定格式:
- ❌ 错误: "帮我分析这段自我介绍"
- ✅ 正确: "将以下自我介绍提取为 JSON 格式,包含 name, skills, experience_years 字段。只输出 JSON,不要其他解释。"

### 3. JSON 解析
在 Python 中使用 `json` 模块解析:
```python
import json

# 将 JSON 字符串转为 Python 字典
data = json.loads('{"name": "张三"}')
print(data["name"])  # 输出: 张三

# 将 Python 字典转为 JSON 字符串
json_str = json.dumps({"name": "李四"}, ensure_ascii=False)
```

## 🚀 练习任务

创建一个程序,能够:
1. 接收用户输入的**乱七八糟的自我介绍**
2. 调用 LLM,让它提取关键信息
3. 强制 LLM 输出 **纯 JSON 格式**
4. 在 Python 中解析 JSON,并美化输出

## 💡 关键挑战

**问题**: AI 有时会输出:
```
好的,我帮你整理了:
{"name": "张三", "skills": ["Python"]}
希望对你有帮助!
```

**解决方案**: 
- 在 System Prompt 中**强调**只输出 JSON
- 使用正则表达式提取 JSON 部分
- 添加错误处理和重试机制

---

现在打开 `resume_parser.py` 开始编程!
