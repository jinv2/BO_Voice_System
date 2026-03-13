#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(c) 2026 Shensi-ST / 天算AI实验室. All Rights Reserved.
Project: 驳 · 万象智能体 (Borg Universal Agent)
Identity: Shensist Matrix Core Agent
"""
"""
BO Project Organizer Test - 测试ProjectOrganizer功能
验证目录熵值重置和级联归档
"""

import asyncio
import sys
import os
import tempfile
import shutil
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bo_core import ProjectOrganizer

def create_test_files():
    """创建测试文件"""
    test_files = {
        "example.py": "# Python test file",
        "readme.md": "# Test README",
        "config.json": '{"test": true}',
        "setup.sh": "#!/bin/bash\necho 'test'",
        "notes.txt": "Test notes",
        "settings.yaml": "debug: true",
        "misc.xyz": "Unknown file type"
    }
    
    for filename, content in test_files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ 创建了 {len(test_files)} 个测试文件")

async def test_project_organizer():
    """测试ProjectOrganizer"""
    print("🧪 测试 ProjectOrganizer")
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "bo_test"
        test_dir.mkdir()
        
        # 切换到测试目录
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        try:
            # 创建测试文件
            create_test_files()
            
            # 初始化ProjectOrganizer
            organizer = ProjectOrganizer(str(test_dir))
            
            print(f"\n📁 测试目录: {test_dir}")
            print("📋 整理前文件:")
            for file in test_dir.iterdir():
                if file.is_file():
                    print(f"  - {file.name}")
            
            # 执行整理
            print("\n🗂️  执行目录熵值重置...")
            result = organizer.organize_current_dir()
            
            print(f"\n📊 整理结果: {result}")
            
            if result.get("status") == "success":
                print("✅ 目录整理成功")
                
                # 检查整理后的目录结构
                print("\n📁 整理后目录结构:")
                for item in test_dir.iterdir():
                    if item.is_dir():
                        print(f"  📂 {item.name}/")
                        for file in item.iterdir():
                            if file.is_file():
                                print(f"    📄 {file.name}")
                    elif item.is_file():
                        print(f"  📄 {item.name}")
                
                # 验证文件分类
                expected_dirs = {"src", "docs", "config", "scripts", "misc"}
                actual_dirs = {item.name for item in test_dir.iterdir() if item.is_dir()}
                
                print(f"\n🔍 验证结果:")
                print(f"  期望目录: {expected_dirs}")
                print(f"  实际目录: {actual_dirs}")
                print(f"  匹配度: {len(expected_dirs & actual_dirs)}/{len(expected_dirs)}")
                
            else:
                print("❌ 目录整理失败")
                print(f"错误: {result.get('message')}")
        
        finally:
            # 恢复原目录
            os.chdir(original_cwd)

async def test_bo_core_integration():
    """测试BO核心集成"""
    print("\n🧪 测试 BOVoiceCore 集成")
    
    from bo_core import BOVoiceCore
    
    core = BOVoiceCore()
    
    # 测试整理接口
    print("🔧 测试核心整理接口...")
    result = core.organize_current_directory()
    
    print(f"📊 核心整理结果: {result}")
    
    if result.get("status") == "success":
        print("✅ 核心集成正常")
        print(f"  归档文件: {result.get('organized_files', 0)} 个")
        print(f"  创建目录: {result.get('created_directories', [])}")
    else:
        print("❌ 核心集成异常")

async def main():
    """主测试函数"""
    print("📜 驳 (BO) ProjectOrganizer 功能测试")
    print("=" * 50)
    
    try:
        await test_project_organizer()
        await test_bo_core_integration()
        
        print("\n✅ 所有测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
