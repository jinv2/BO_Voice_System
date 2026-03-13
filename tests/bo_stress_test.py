import sys
import os
import time

# 确保路径正确
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bo_skills_matrix import BOSkillsMatrix
from bo_brain import BOBrain
from bo_interpreter import BOInterpreter

def run_tests():
    print("--- 🏁 BO Intelligence Stress Test Ignition ---")
    
    matrix = BOSkillsMatrix()
    brain = BOBrain(matrix)
    interpreter = BOInterpreter(matrix, brain)
    
    test_cases = [
        "帮我剪辑这个高清视频！",
        "我想编辑这个 PDF 合同",
        "列出今天午饭菜单",
        "为新客户神思矩阵建立项目架构",
        "这是一句随机的无法理解指令"
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n[Advisory Test {i}] Query: '{query}'")
        print("Executive Reasoning...")
        result = interpreter.parse_and_execute(query)
        
        status = result.get("status")
        message = result.get("message", "")
        
        if status == "success":
            print(f"✅ Success Feedback: {message}")
        elif status == "advisory":
            print(f"💡 Advisory Advice Triggered:\n{message}")
        elif status == "error":
            print(f"❌ Error Guard Triggered: {message}")
        else:
            print(f"⚠️ Unknown State: {result}")

    print("\n--- 🏁 Test Suite Completed ---")

if __name__ == "__main__":
    run_tests()
