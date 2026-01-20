# -*- coding: utf-8 -*-
"""
Day 4: MCP Server - 文件管理器
使用 FastMCP 创建一个简单的文件管理 MCP 服务器
"""
import os
from pathlib import Path
from datetime import datetime
from fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("文件管理器")

# ==========================================
# 辅助函数
# ==========================================

def format_size(size_bytes: int) -> str:
    """将字节大小转换为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

# ==========================================
# 核心函数 (不带装饰器,用于测试)
# ==========================================

def _list_files(directory: str) -> list[str]:
    """列出指定目录中的所有文件和子目录"""
    dir_path = Path(directory).expanduser().resolve()
    
    if not dir_path.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")
    
    if not dir_path.is_dir():
        raise NotADirectoryError(f"不是目录: {directory}")
    
    try:
        items = []
        for item in dir_path.iterdir():
            if item.is_dir():
                items.append(f"📁 {item.name}/")
            else:
                items.append(f"📄 {item.name}")
        
        return sorted(items)
    except PermissionError:
        raise PermissionError(f"没有权限访问目录: {directory}")

def _read_file(filepath: str, max_lines: int = 100) -> str:
    """读取文件内容"""
    file_path = Path(filepath).expanduser().resolve()
    
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    if not file_path.is_file():
        raise IsADirectoryError(f"不是文件: {filepath}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    lines.append(f"\n... (文件太长,已截断,仅显示前 {max_lines} 行)")
                    break
                lines.append(line.rstrip('\n'))
            
            return '\n'.join(lines)
    except PermissionError:
        raise PermissionError(f"没有权限读取文件: {filepath}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(
            'utf-8', b'', 0, 1,
            f"文件不是文本文件或编码不是 UTF-8: {filepath}"
        )

def _get_file_info(filepath: str) -> dict:
    """获取文件或目录的详细信息"""
    path = Path(filepath).expanduser().resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"路径不存在: {filepath}")
    
    stat = path.stat()
    
    return {
        "name": path.name,
        "path": str(path),
        "type": "directory" if path.is_dir() else "file",
        "size": stat.st_size,
        "size_human": format_size(stat.st_size),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
    }

# ==========================================
# MCP 工具 (带装饰器,用于 MCP 协议)
# ==========================================

@mcp.tool()
def list_files(directory: str) -> list[str]:
    """
    列出指定目录中的所有文件和子目录
    
    Args:
        directory: 目录路径,例如: /home/user/documents 或 ./data
    
    Returns:
        文件和目录名称列表
    """
    return _list_files(directory)

@mcp.tool()
def read_file(filepath: str, max_lines: int = 100) -> str:
    """
    读取文件内容
    
    Args:
        filepath: 文件路径,例如: /home/user/document.txt
        max_lines: 最多读取的行数,默认 100 行
    
    Returns:
        文件内容(文本)
    """
    return _read_file(filepath, max_lines)

@mcp.tool()
def get_file_info(filepath: str) -> dict:
    """
    获取文件或目录的详细信息
    
    Args:
        filepath: 文件或目录路径
    
    Returns:
        包含文件信息的字典
    """
    return _get_file_info(filepath)

# ==========================================
# 运行服务器
# ==========================================

if __name__ == "__main__":
    mcp.run()
