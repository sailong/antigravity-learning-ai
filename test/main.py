import argparse
import asyncio
import os
import sys
from agent import AnalysisAgent

# Add parent directory to path to allow importing modules from sibling directories if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def main():
    parser = argparse.ArgumentParser(description="文件内容分析程序")
    parser.add_argument("--input", "-i", type=str, required=True, help="输入文件的路径")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"错误: 未找到: {input_path}")
        return

    files_to_process = []
    if os.path.isdir(input_path):
        print(f"📂 检测到目录输入，正在扫描文件...")
        for root, _, files in os.walk(input_path):
            for file in files:
                if not file.startswith('.') and not file.endswith('_analysis_output'): # 忽略隐藏文件和输出目录
                    files_to_process.append(os.path.join(root, file))
    else:
        files_to_process.append(input_path)

    agent = AnalysisAgent()
    
    for file_path in files_to_process:
        print(f"\n{'='*50}")
        print(f"正在处理文件: {file_path}")
        
        # 根据文件名创建输出目录
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # 如果是目录输入，我们在同级目录下创建 output 文件夹
        output_dir = os.path.join(os.path.dirname(file_path), f"{base_name}_analysis_output")
        os.makedirs(output_dir, exist_ok=True)
        print(f"📂 输出目录: {output_dir}")
        
        await agent.analyze_file(file_path, output_dir)

if __name__ == "__main__":
    asyncio.run(main())
