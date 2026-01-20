# -*- coding: utf-8 -*-
import os
import sys
import locale
import json

# 设置环境编码
os.environ['PYTHONIOENCODING'] = 'utf-8'
locale.setlocale(locale.LC_ALL, '')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

from openai import OpenAI

# ==========================================
# 🔧 配置
# ==========================================

api_key = os.getenv("OPENAI_API_KEY", "lm-studio")
base_url = "http://127.0.0.1:33333/v1"
model_name = "qwen/qwen3-vl-8b"

client = OpenAI(api_key=api_key, base_url=base_url)

# ==========================================
# 📦 定义可用的函数 (工具箱)
# ==========================================

def get_weather(city):
    """获取天气信息 (模拟数据)"""
    weather_data = {
        "北京": {"weather": "晴天", "temperature": "15°C", "humidity": "45%"},
        "上海": {"weather": "多云", "temperature": "18°C", "humidity": "60%"},
        "广州": {"weather": "小雨", "temperature": "22°C", "humidity": "75%"},
        "深圳": {"weather": "晴天", "temperature": "25°C", "humidity": "55%"}
    }
    
    if city in weather_data:
        data = weather_data[city]
        return json.dumps(data, ensure_ascii=False)
    else:
        return json.dumps({"error": f"{city}的天气数据暂时无法获取"}, ensure_ascii=False)

def calculate(expression):
    """计算数学表达式"""
    try:
        # 安全的计算,只允许基本运算
        allowed_chars = set("0123456789+-*/.()")
        if not all(c in allowed_chars or c.isspace() for c in expression):
            return json.dumps({"error": "表达式包含不允许的字符"}, ensure_ascii=False)
        
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"计算错误: {str(e)}"}, ensure_ascii=False)

# 函数注册表
AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather,
    "calculate": calculate
}

# ==========================================
# 🛠️ 定义函数描述 (告诉 AI 有哪些工具)
# ==========================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的实时天气信息,包括天气状况、温度和湿度",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称,例如: 北京、上海、广州、深圳"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式,支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式,例如: 123 + 456, (10 * 5) - 3"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# ==========================================
# 🤖 主函数: 处理用户问题
# ==========================================

def chat_with_function_calling(user_question):
    """
    使用 Function Calling 处理用户问题
    """
    print(f"\n👤 用户: {user_question}")
    print("=" * 60)
    
    # 初始化对话历史
    messages = [
        {
            "role": "system",
            "content": "你是一个智能助手,可以帮助用户查询天气和进行数学计算。当用户询问天气或需要计算时,请使用相应的工具。"
        },
        {
            "role": "user",
            "content": user_question
        }
    ]
    
    # 第一次调用 AI
    print("🤖 AI 正在分析问题...")
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # 让 AI 自动决定是否调用函数
            temperature=0.3
        )
        
        assistant_message = response.choices[0].message
        
        # 检查 AI 是否要调用函数
        if assistant_message.tool_calls:
            print(f"💡 AI 决定调用函数!")
            
            # 将 AI 的回复加入历史
            messages.append(assistant_message)
            
            # 处理每个函数调用
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"\n📞 调用函数: {function_name}")
                print(f"📋 参数: {json.dumps(function_args, ensure_ascii=False)}")
                
                # 执行函数
                function_to_call = AVAILABLE_FUNCTIONS.get(function_name)
                if function_to_call:
                    function_result = function_to_call(**function_args)
                    print(f"⚙️  执行结果: {function_result}")
                    
                    # 将函数结果加入对话历史
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": function_result
                    })
                else:
                    print(f"❌ 错误: 函数 '{function_name}' 不存在")
            
            # 第二次调用 AI,让它根据函数结果生成最终回复
            print("\n🤖 AI 正在生成最终回复...")
            second_response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.3
            )
            
            final_reply = second_response.choices[0].message.content
            print(f"\n💬 AI 回复: {final_reply}")
            
        else:
            # AI 不需要调用函数,直接回复
            print(f"\n💬 AI 回复: {assistant_message.content}")
    
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

# ==========================================
# 🚀 主程序
# ==========================================

def main():
    print("=" * 60)
    print("🤖 Function Calling 智能助手")
    print("=" * 60)
    print("\n我可以帮你:")
    print("  1. 查询天气 (支持: 北京、上海、广州、深圳)")
    print("  2. 进行数学计算")
    print("\n输入 'quit' 退出程序\n")
    
    # 测试问题
    test_questions = [
        "北京今天天气怎么样?",
        "帮我算一下 (123 + 456) * 2",
        "上海和广州哪个城市温度更高?"
    ]
    
    print("📝 示例问题:")
    for i, q in enumerate(test_questions, 1):
        print(f"  {i}. {q}")
    
    while True:
        print("\n" + "-" * 60)
        user_input = input("\n💬 请输入问题 (或输入 quit 退出): ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("\n👋 再见!")
            break
        
        if not user_input:
            print("⚠️  输入不能为空")
            continue
        
        chat_with_function_calling(user_input)

if __name__ == "__main__":
    main()
