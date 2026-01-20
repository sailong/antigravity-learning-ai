# -*- coding: utf-8 -*-
import os
import sys
import locale
import json
import re

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
# 🔧 配置区域
# ==========================================

api_key = os.getenv("OPENAI_API_KEY", "lm-studio")
base_url = "http://127.0.0.1:33333/v1"
model_name = "qwen/qwen3-vl-8b"

# ==========================================
# 🤖 初始化客户端
# ==========================================

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def extract_json_from_text(text):
    """
    从 AI 的回复中提取 JSON 部分
    因为 AI 有时会输出额外的解释文字
    """
    # 尝试直接解析整个文本
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # 尝试提取 JSON 对象 (大括号包裹的部分)
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    # 如果都失败了,返回 None
    return None

def parse_resume(messy_intro):
    """
    将乱七八糟的自我介绍解析为结构化 JSON
    """
    # 🔑 关键: System Prompt 必须非常明确
    system_prompt = """你是一个专业的简历信息提取助手。
你的任务是从用户提供的自我介绍中提取关键信息,并以 JSON 格式输出。

输出格式要求:
{
  "name": "姓名",
  "skills": ["技能1", "技能2", "技能3"],
  "experience_years": 工作年限(数字),
  "education": "学历",
  "position": "期望职位"
}

重要规则:
1. 只输出 JSON,不要任何其他文字
2. 如果某个字段无法从介绍中提取,使用 null
3. skills 必须是数组
4. experience_years 必须是数字
5. 不要添加任何解释或客套话"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"请提取以下自我介绍的信息:\n\n{messy_intro}"}
    ]

    try:
        print("🤖 正在调用 AI 提取信息...")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,  # 降低温度,让输出更确定
            stream=False
        )

        ai_reply = response.choices[0].message.content
        print(f"\n📄 AI 原始回复:\n{ai_reply}\n")
        print("-" * 60)

        # 提取 JSON
        parsed_data = extract_json_from_text(ai_reply)
        
        if parsed_data:
            print("✅ JSON 解析成功!")
            return parsed_data
        else:
            print("❌ 无法从 AI 回复中提取有效的 JSON")
            return None

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("=" * 60)
    print("📋 简历信息提取器 (Day 2 练习)")
    print("=" * 60)
    print("\n请输入一段乱七八糟的自我介绍,我会帮你整理成结构化数据。")
    print("提示: 可以包含姓名、技能、工作年限、学历、期望职位等信息。")
    print("输入 'quit' 退出程序。\n")

    while True:
        print("-" * 60)
        user_input = input("\n📝 请输入自我介绍 (或输入 quit 退出): \n")
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("\n👋 再见!")
            break
        
        if not user_input.strip():
            print("⚠️  输入不能为空,请重新输入。")
            continue

        # 调用 AI 解析
        result = parse_resume(user_input)
        
        if result:
            print("\n" + "=" * 60)
            print("📊 提取结果 (结构化数据):")
            print("=" * 60)
            # 美化输出 JSON
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("=" * 60)
            
            # 展示如何使用提取的数据
            print("\n💡 如何使用这些数据:")
            print(f"  - 姓名: {result.get('name', '未知')}")
            print(f"  - 技能数量: {len(result.get('skills', []))}")
            print(f"  - 工作年限: {result.get('experience_years', 0)} 年")
            print(f"  - 学历: {result.get('education', '未知')}")
            print(f"  - 期望职位: {result.get('position', '未知')}")
        else:
            print("\n⚠️  解析失败,请尝试提供更清晰的自我介绍。")

if __name__ == "__main__":
    main()
