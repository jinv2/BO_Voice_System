"""
(c) 2026 Shensi-ST / 天算AI实验室. All Rights Reserved.
Project: 驳 · 万象智能体 (Borg Universal Agent)
Identity: Shensist Matrix Core Agent
"""
import re

class BOInterpreter:
    """驳 · 意图智能层 (L2 Intelligence Layer)"""
    def __init__(self, skills_matrix, brain):
        self.matrix = skills_matrix
        self.brain = brain
        # 意图映射表 (模糊匹配核心)
        self.rules = {
            r"搜索\s*(.*)": ("search", "query"),
            r"查找\s*(.*)": ("search", "query"),
            r"打开浏览器": ("browser", None),
            r"打开终端": ("terminal", None),
            r"打开文件夹": ("file_manager", None),
            r"截图": ("screenshot", None),
            r"复制": ("copy", None),
            r"粘贴": ("paste", None),
            r"音量\+": ("vol_up", None),
            r"音量增": ("vol_up", None),
            r"音量-": ("vol_down", None),
            r"音量减": ("vol_down", None),
            r"锁屏": ("lock", None),
            r"整理": ("organize", None),
            r"新建文件夹\s*(.*)": ("new_folder", "name")
        }

    def parse_and_execute(self, text):
        """将文字解析为意图，若无显式意图则交由万象大脑规划"""
        text = text.strip()
        if not text: return {"status": "none"}

        for pattern, (intent, param_name) in self.rules.items():
            match = re.search(pattern, text)
            if match:
                params = {}
                if param_name and match.groups():
                    params[param_name] = match.group(1).strip()
                return self.matrix.execute(intent, **params)

        # 万象归一：无匹配意图时，触动逻辑规划引擎
        print(f"Borg-▲: No explicit intent. Handover to BOBrain -> {text}")
        return self.brain.think_and_execute(text)
