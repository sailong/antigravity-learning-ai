# -*- coding: utf-8 -*-
"""
Day 3 练习: Function Calling 伪代码演示
这个脚本帮助你理解 Function Calling 的基本原理
不使用真实的 AI API,而是手动模拟整个流程
"""
import json

print("=" * 60)
print("🎓 Day 3: Function Calling 原理演示 (伪代码)")
print("=" * 60)

# ==========================================
# 步骤 1: 定义可用的函数
# ==========================================
print("\n【步骤 1】定义可用的函数")
print("-" * 60)

def get_weather(city):
    """获取天气信息 (模拟数据)"""
    weather_data = {
        "北京": "晴天,温度 15°C",
        "上海": "多云,温度 18°C",
        "广州": "小雨,温度 22°C"
    }
    return weather_data.get(city, f"{city}的天气数据暂时无法获取")

def calculate(expression):
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"

# 函数注册表 (模拟 AI 可以调用的工具)
AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather,
    "calculate": calculate
}

print("✅ 已注册函数:")
for func_name in AVAILABLE_FUNCTIONS.keys():
    print(f"  - {func_name}")

# ==========================================
# 步骤 2: 定义函数描述 (告诉 AI 有哪些工具)
# ==========================================
print("\n【步骤 2】定义函数描述")
print("-" * 60)

function_definitions = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "city": {
                "type": "string",
                "description": "城市名称,例如: 北京、上海、广州"
            }
        }
    },
    {
        "name": "calculate",
        "description": "计算数学表达式",
        "parameters": {
            "expression": {
                "type": "string",
                "description": "数学表达式,例如: 123 + 456"
            }
        }
    }
]

print("✅ 函数描述已定义:")
for func_def in function_definitions:
    print(f"  - {func_def['name']}: {func_def['description']}")

# ==========================================
# 步骤 3: 模拟用户提问
# ==========================================
print("\n【步骤 3】模拟用户提问")
print("-" * 60)

test_questions = [
    "北京今天天气怎么样?",
    "帮我算一下 123 * 456",
    "上海的天气如何?"
]

for question in test_questions:
    print(f"\n👤 用户: {question}")
    
    # ==========================================
    # 步骤 4: AI 分析问题并决定调用哪个函数
    # ==========================================
    print("🤖 AI 思考中...")
    
    # 这里我们手动模拟 AI 的决策
    # 在真实场景中,这是 AI 自动完成的
    if "天气" in question:
        # 提取城市名称 (简化处理)
        city = None
        for c in ["北京", "上海", "广州"]:
            if c in question:
                city = c
                break
        
        ai_decision = {
            "function": "get_weather",
            "arguments": {"city": city or "北京"}
        }
    elif "算" in question or "计算" in question:
        # 提取数学表达式 (简化处理)
        import re
        match = re.search(r'(\d+\s*[\+\-\*/]\s*\d+)', question)
        expression = match.group(1) if match else "1+1"
        
        ai_decision = {
            "function": "calculate",
            "arguments": {"expression": expression}
        }
    else:
        ai_decision = None
    
    if ai_decision:
        print(f"💡 AI 决定: 调用函数 '{ai_decision['function']}'")
        print(f"📋 参数: {json.dumps(ai_decision['arguments'], ensure_ascii=False)}")
        
        # ==========================================
        # 步骤 5: 执行函数
        # ==========================================
        func_name = ai_decision["function"]
        func_args = ai_decision["arguments"]
        
        # 获取函数
        func = AVAILABLE_FUNCTIONS.get(func_name)
        
        if func:
            # 执行函数
            result = func(**func_args)
            print(f"⚙️  执行结果: {result}")
            
            # ==========================================
            # 步骤 6: AI 根据结果生成最终回复
            # ==========================================
            # 在真实场景中,这里会再次调用 AI
            # 让 AI 根据函数结果生成用户友好的回复
            print(f"🤖 AI 最终回复: {result}")
        else:
            print(f"❌ 错误: 函数 '{func_name}' 不存在")
    else:
        print("🤖 AI: 抱歉,我不知道如何回答这个问题。")

# ==========================================
# 总结
# ==========================================
print("\n" + "=" * 60)
print("📚 Function Calling 流程总结")
print("=" * 60)
print("""
1. 定义函数 (你的代码)
   ↓
2. 定义函数描述 (告诉 AI 有哪些工具)
   ↓
3. 用户提问
   ↓
4. AI 分析并决定调用哪个函数
   ↓
5. 你的代码执行函数
   ↓
6. 将结果返回给 AI
   ↓
7. AI 生成最终回复

关键点:
- AI 不直接执行函数,只是"建议"调用
- 你的代码负责真正执行,保证安全性
- 这是一个多轮对话的过程
""")
print("=" * 60)
