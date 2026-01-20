# -*- coding: utf-8 -*-
import os
import sys
import locale

# 设置环境编码
os.environ['PYTHONIOENCODING'] = 'utf-8'
locale.setlocale(locale.LC_ALL, '')

# 确保标准输入输出使用 UTF-8 编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

from openai import OpenAI

# ==========================================
# 🔧 配置区域 (请按照你的实际情况修改)
# ==========================================

# 1. 本地 LLM Studio 的 API Key (通常可以是任意值)
api_key = os.getenv("OPENAI_API_KEY", "lm-studio")

# 2. 本地 LLM 服务地址
base_url = "http://127.0.0.1:33333/v1"

# 3. 模型名称 (根据你的本地 LLM 服务支持的模型)
# 可选: qwen/qwen3-vl-8b, qwen/qwen3-vl-30b
model_name = "qwen/qwen3-vl-8b"

# ==========================================
# 🤖 初始化客户端
# ==========================================

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def chat_with_hiring_manager():
    print("------------------------------------------------------")
    print("👨‍💼 面试官: 这里的简历堆积如山，你最好言简意赅。请进。")
    print("------------------------------------------------------")

    # 定义"人设" (System Prompt)
    system_prompt = "你是一位性格严厉、不苟言笑的技术招聘经理。你只关心求职者的技术能力和过往经验。无论用户说什么，你都要保持这种专业且略带挑剔的口吻。不要跳出角色。"

    # 简单的对话历史 (让 AI 记得之前的对话)
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    while True:
        try:
            # 获取用户输入
            user_input = input("\n👤 求职者 (你): ")
            
            # 退出条件
            if user_input.lower() in ["exit", "quit", "退出", "再见"]:
                print("\n👨‍💼 面试官: 行了，今天的面试到此结束。回去等通知吧。")
                break

            # 将用户的话加入历史
            messages.append({"role": "user", "content": user_input})

            # 调用大模型 (API Call)
            # 关键: 使用 encoding='utf-8' 确保请求正确编码
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7,  # 0.7 稍显灵活，0.2 更加严谨
                stream=False
            )

            # 获取 AI 的回复
            ai_reply = response.choices[0].message.content

            # 显示回复
            print(f"\n👨‍💼 面试官: {ai_reply}")

            # 将 AI 的回复也加入历史，形成多轮对话
            messages.append({"role": "assistant", "content": ai_reply})

        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            print(f"错误类型: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            print("\n请检查你的 API Key 和网络配置。")
            break

if __name__ == "__main__":
    chat_with_hiring_manager()
