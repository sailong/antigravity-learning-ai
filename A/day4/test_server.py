# -*- coding: utf-8 -*-
"""
测试 MCP Server 的工具
不使用 fastmcp dev,而是直接调用工具函数进行测试
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from file_server import _list_files, _read_file, _get_file_info

print("=" * 60)
print("🧪 测试 MCP Server 工具")
print("=" * 60)

# ==========================================
# 测试 1: list_files
# ==========================================
print("\n【测试 1】list_files - 列出目录文件")
print("-" * 60)

try:
    test_dir = "./test_data"
    print(f"📂 测试目录: {test_dir}")
    
    files = _list_files(test_dir)
    print(f"\n✅ 找到 {len(files)} 个项目:")
    for file in files:
        print(f"  {file}")
except Exception as e:
    print(f"❌ 错误: {e}")

# ==========================================
# 测试 2: read_file
# ==========================================
print("\n【测试 2】read_file - 读取文件内容")
print("-" * 60)

try:
    test_file = "./test_data/file1.txt"
    print(f"📄 测试文件: {test_file}")
    
    content = _read_file(test_file)
    print(f"\n✅ 文件内容:")
    print(content)
except Exception as e:
    print(f"❌ 错误: {e}")

# ==========================================
# 测试 3: get_file_info
# ==========================================
print("\n【测试 3】get_file_info - 获取文件信息")
print("-" * 60)

try:
    test_file = "./test_data/file1.txt"
    print(f"📄 测试文件: {test_file}")
    
    info = _get_file_info(test_file)
    print(f"\n✅ 文件信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
except Exception as e:
    print(f"❌ 错误: {e}")

# ==========================================
# 测试 4: 错误处理
# ==========================================
print("\n【测试 4】错误处理 - 测试不存在的文件")
print("-" * 60)

try:
    non_existent = "./non_existent_file.txt"
    print(f"📄 测试文件: {non_existent}")
    
    content = _read_file(non_existent)
    print(f"❌ 应该抛出错误,但没有!")
except FileNotFoundError as e:
    print(f"✅ 正确捕获错误: {e}")
except Exception as e:
    print(f"⚠️  捕获了其他错误: {e}")

print("\n" + "=" * 60)
print("🎉 测试完成!")
print("=" * 60)

# ==========================================
# 总结
# ==========================================
print("\n📚 MCP Server 工具总结:")
print("  1. list_files(directory) - 列出目录内容")
print("  2. read_file(filepath, max_lines) - 读取文件")
print("  3. get_file_info(filepath) - 获取文件信息")
print("\n💡 这些工具可以通过 MCP 协议被 AI Agent 调用!")
