# -*- coding: utf-8 -*-
"""
Day 2 练习: JSON 基础操作
这个脚本帮助你熟悉 JSON 的基本操作
"""
import json

print("=" * 60)
print("📚 Day 2 练习: JSON 基础操作")
print("=" * 60)

# ==========================================
# 练习 1: JSON 字符串 -> Python 对象
# ==========================================
print("\n【练习 1】JSON 字符串 -> Python 对象")
print("-" * 60)

json_string = '''
{
  "name": "张伟",
  "age": 28,
  "skills": ["Python", "Java", "JavaScript"],
  "education": {
    "degree": "本科",
    "major": "计算机科学"
  },
  "is_available": true,
  "salary_expectation": null
}
'''

# 解析 JSON
data = json.loads(json_string)

print(f"类型: {type(data)}")
print(f"姓名: {data['name']}")
print(f"年龄: {data['age']}")
print(f"第一个技能: {data['skills'][0]}")
print(f"学历: {data['education']['degree']}")
print(f"专业: {data['education']['major']}")
print(f"是否可入职: {data['is_available']}")
print(f"期望薪资: {data['salary_expectation']}")

# ==========================================
# 练习 2: Python 对象 -> JSON 字符串
# ==========================================
print("\n【练习 2】Python 对象 -> JSON 字符串")
print("-" * 60)

person = {
    "name": "李明",
    "age": 25,
    "skills": ["React", "Vue", "Node.js"],
    "projects": [
        {
            "name": "电商平台",
            "role": "前端开发",
            "duration": "6个月"
        },
        {
            "name": "管理系统",
            "role": "全栈开发",
            "duration": "1年"
        }
    ]
}

# 转换为 JSON (紧凑格式)
json_compact = json.dumps(person, ensure_ascii=False)
print("紧凑格式:")
print(json_compact)

# 转换为 JSON (美化格式)
json_pretty = json.dumps(person, ensure_ascii=False, indent=2)
print("\n美化格式:")
print(json_pretty)

# ==========================================
# 练习 3: 处理嵌套 JSON
# ==========================================
print("\n【练习 3】处理嵌套 JSON")
print("-" * 60)

resume = {
    "candidate": {
        "name": "王芳",
        "contact": {
            "email": "wangfang@example.com",
            "phone": "13800138000"
        }
    },
    "work_experience": [
        {
            "company": "A公司",
            "position": "Python工程师",
            "years": 2
        },
        {
            "company": "B公司",
            "position": "数据分析师",
            "years": 1
        }
    ]
}

print(f"候选人姓名: {resume['candidate']['name']}")
print(f"邮箱: {resume['candidate']['contact']['email']}")
print(f"第一份工作公司: {resume['work_experience'][0]['company']}")
print(f"第一份工作职位: {resume['work_experience'][0]['position']}")

# 遍历工作经历
print("\n工作经历:")
for exp in resume['work_experience']:
    print(f"  - {exp['company']}: {exp['position']} ({exp['years']}年)")

# ==========================================
# 练习 4: 错误处理
# ==========================================
print("\n【练习 4】错误处理")
print("-" * 60)

# 错误的 JSON 字符串
invalid_json = '{"name": "张三", "age": 25'  # 缺少右括号

try:
    data = json.loads(invalid_json)
    print("解析成功!")
except json.JSONDecodeError as e:
    print(f"❌ JSON 解析失败: {e}")
    print(f"错误位置: 第 {e.lineno} 行, 第 {e.colno} 列")

# ==========================================
# 练习 5: 数据验证
# ==========================================
print("\n【练习 5】数据验证")
print("-" * 60)

def validate_resume(data):
    """验证简历数据是否完整"""
    required_fields = ["name", "skills", "experience_years"]
    
    for field in required_fields:
        if field not in data:
            return False, f"缺少必要字段: {field}"
    
    # 验证数据类型
    if not isinstance(data["skills"], list):
        return False, "skills 必须是数组"
    
    if not isinstance(data["experience_years"], (int, float)):
        return False, "experience_years 必须是数字"
    
    return True, "验证通过"

# 测试数据
test_data_1 = {
    "name": "测试1",
    "skills": ["Python"],
    "experience_years": 3
}

test_data_2 = {
    "name": "测试2",
    "skills": "Python"  # 错误: 应该是数组
}

test_data_3 = {
    "name": "测试3"
    # 错误: 缺少 skills 和 experience_years
}

for i, test_data in enumerate([test_data_1, test_data_2, test_data_3], 1):
    is_valid, message = validate_resume(test_data)
    status = "✅" if is_valid else "❌"
    print(f"{status} 测试数据 {i}: {message}")

# ==========================================
# 练习 6: 实用技巧
# ==========================================
print("\n【练习 6】实用技巧")
print("-" * 60)

# 技巧 1: 安全获取值 (使用 get 方法)
data = {"name": "张三"}
print(f"姓名: {data.get('name', '未知')}")
print(f"年龄: {data.get('age', '未知')}")  # 不存在的键,返回默认值

# 技巧 2: 检查键是否存在
if "email" in data:
    print(f"邮箱: {data['email']}")
else:
    print("未提供邮箱")

# 技巧 3: 合并字典
default_config = {"timeout": 30, "retry": 3}
user_config = {"timeout": 60}
final_config = {**default_config, **user_config}
print(f"\n合并后的配置: {final_config}")

print("\n" + "=" * 60)
print("🎉 练习完成! 你已经掌握了 JSON 的基本操作!")
print("=" * 60)
