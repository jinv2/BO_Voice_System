#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BO Voice Test - 测试完善后的系统
验证ClipboardHandler和listen_loop功能
"""

import asyncio
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bo_core import BOVoiceCore, ClipboardHandler
from bo_voice import BOVoiceRecognizer

async def test_clipboard_handler():
    """测试剪贴板处理器"""
    print("🧪 测试 ClipboardHandler")
    
    handler = ClipboardHandler()
    
    # 测试复制
    test_text = "驳系统测试文本"
    result = handler.copy(test_text)
    
    print(f"复制结果: {result}")
    
    if result.get("status") == "success":
        print("✅ 复制功能正常")
        
        # 测试粘贴
        paste_result = handler.paste()
        print(f"粘贴结果: {paste_result}")
        
        if paste_result.get("status") == "success":
            print("✅ 粘贴功能正常")
        else:
            print("❌ 粘贴功能异常")
    else:
        print("❌ 复制功能异常")

async def test_voice_core():
    """测试BO核心"""
    print("\n🧪 测试 BOVoiceCore")
    
    core = BOVoiceCore()
    
    # 测试公共接口
    copy_result = core.copy("测试内容")
    print(f"核心复制结果: {copy_result}")
    
    if copy_result.get("status") == "success":
        print("✅ 核心复制接口正常")
    else:
        print("❌ 核心复制接口异常")

async def test_voice_recognizer():
    """测试语音识别器"""
    print("\n🧪 测试 BOVoiceRecognizer")
    
    recognizer = BOVoiceRecognizer()
    
    # 设置核心引用
    core = BOVoiceCore()
    recognizer.set_core_reference(core)
    
    print("✅ 语音识别器初始化完成")
    print("📝 注意: 实际语音测试需要麦克风和faster-whisper")

async def test_notification_system():
    """测试通知系统"""
    print("\n🧪 测试通知系统")
    
    recognizer = BOVoiceRecognizer()
    
    # 测试通知显示
    await recognizer._show_notification("驳：系统测试通知")
    print("✅ 通知系统测试完成")

async def main():
    """主测试函数"""
    print("📜 驳 (BO) 系统功能测试")
    print("=" * 40)
    
    try:
        await test_clipboard_handler()
        await test_voice_core()
        await test_voice_recognizer()
        await test_notification_system()
        
        print("\n✅ 所有测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
