"""
(c) 2026 Shensi-ST / 天算AI实验室. All Rights Reserved.
Project: 驳 · 万象智能体 (Borg Universal Agent)
Identity: Shensist Matrix Core Agent
"""
import sys
import os
import threading
import logging

# 核心路径锁定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'src'))

from bo_ui import BOStatusUI
from bo_interpreter import BOInterpreter
from bo_brain import BOBrain
from bo_skills_matrix import BOSkillsMatrix

class BOAgent:
    """驳 · 万象智能体 (Universal Agent Core)"""
    def __init__(self):
        # 建立三重架构 L1-L3 (万象增强版)
        self.matrix = BOSkillsMatrix() # L3: Execution
        self.brain = BOBrain(self.matrix) # L2-Logic: Reasoning
        self.interpreter = BOInterpreter(self.matrix, self.brain) # L2-Parser
        self.ui = BOStatusUI(callback=self.input_trigger) # L1: Sensing
        
        print("🟢 BO · Universal Agent Matrix Active. L1-L3 Ascended.")

    def input_trigger(self, text):
        """L1 -> L2 手动触发映射"""
        print(f"Borg-▲: Logic Trigger -> {text}")
        # 启动异步线程保护 UI 响应
        threading.Thread(target=self.process_command, args=(text,), daemon=True).start()

    def process_command(self, text):
        """L2 -> L3 执行链"""
        try:
            result = self.interpreter.parse_and_execute(text)
            msg = result.get("message", "执行完毕")
            
            # 物理反馈回传 UI (L3 -> L1)
            self.ui.set_result(msg)
            
            if result.get("status") == "success":
                print(f"Borg-▲: Analytical Success -> {msg}")
            elif result.get("status") == "error":
                print(f"Borg-▲: Analysis Error -> {msg}")
            else:
                print(f"Borg-▲: No Intent -> {msg}")
        except Exception as e:
            print(f"Borg-▲: System Fault -> {e}")
            self.ui.set_result(f"系统故障: {e}")

    def start(self):
        self.ui.run()

if __name__ == "__main__":
    try:
        BOAgent().start()
    except KeyboardInterrupt:
        print("\nBorg-▲: Consciousness suspended.")
