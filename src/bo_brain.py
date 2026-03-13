"""
(c) 2026 Shensi-ST / 天算AI实验室. All Rights Reserved.
Project: 驳 · 万象智能体 (Borg Universal Agent)
Identity: Shensist Matrix Core Agent
"""
import subprocess
import re
import os
import platform

class BOBrain:
    """驳 · 万象大脑 (L2 Planning Core) - Cross-Platform Edition"""
    def __init__(self, skills_matrix):
        self.matrix = skills_matrix
        self.os_type = platform.system() # 'Linux', 'Windows', 'Darwin'
        self.is_windows = self.os_type == 'Windows'
        self.is_mac = self.os_type == 'Darwin'
        
        self.context = {
            "os": self.os_type,
            "cwd": os.getcwd(),
            "user": os.getlogin() if not self.is_windows else os.getenv('USERNAME')
        }

    def think_and_execute(self, query):
        """
        万象闭环：
        1. 接收自然语言
        2. 转化为多步 逻辑指令
        3. 无法执行时进行【能力诊断】与【授业建议】
        """
        plan = self._generate_plan(query)
        
        if not plan:
            # 启动能力诊断引擎
            advise = self._diagnose_failure(query)
            return {"status": "advisory", "message": advise}
        
        results = []
        for step in plan:
            if isinstance(step, dict) and "skill" in step:
                res = self.matrix.execute(step["skill"], **step.get("params", {}))
            else:
                res = self.matrix.execute("universal_shell", cmd=step)
            
            msg = res.get("message", "")
            if msg: results.append(msg)
            
        final_summary = "\n".join(results)
        return {"status": "success", "message": final_summary if final_summary.strip() else "商务指令已静默执行完毕。"}

    def _diagnose_failure(self, query):
        """能力诊断引擎：由于缺少环境或技能无法执行时，给出建议 (跨端适配)"""
        q = query.lower()
        
        # 定义包管理器的差异
        pkg_mgr = "sudo apt install" if not self.is_mac else "brew install"
        if self.is_windows: pkg_mgr = "winget install"

        software_map = {
            "视频": {"pkg": "ffmpeg", "desc": "多媒体处理工具", "cmd": f"{pkg_mgr} ffmpeg"},
            "mp4": {"pkg": "ffmpeg", "desc": "多媒体处理工具", "cmd": f"{pkg_mgr} ffmpeg"},
            "pdf": {"pkg": "poppler/libreoffice", "desc": "PDF 处理与办公套件", "cmd": f"{pkg_mgr} poppler libreoffice"},
            "压缩": {"pkg": "7zip", "desc": "归档工具", "cmd": f"{pkg_mgr} 7zip" if not self.is_windows else "winget install 7zip.7zip"},
            "画图": {"pkg": "inkscape", "desc": "专业图像编辑工具", "cmd": f"{pkg_mgr} inkscape"},
            "代码": {"pkg": "vscode", "desc": "代码编辑器", "cmd": f"{pkg_mgr} vscode" if not self.is_windows else "winget install Microsoft.VisualStudioCode"},
            "录屏": {"pkg": "obs-studio", "desc": "专业录屏与直播软件", "cmd": f"{pkg_mgr} obs-studio"},
            "文字识别": {"pkg": "tesseract-ocr", "desc": "光学字符识别引擎", "cmd": f"{pkg_mgr} tesseract-ocr"}
        }

        for key, info in software_map.items():
            if key in q:
                return f"""
【能力受限诊断 - {self.os_type}】
状态：当前环境缺少执行所需软件。
需求：检测到您需要进行 '{key}' 相关操作。
建议安装：{info['pkg']} ({info['desc']})
建议指令：{info['cmd']}
                """.strip()

        return f"抱歉，我暂时无法在 {self.os_type} 环境下理解或执行指令: '{query}'。"

    def _generate_plan(self, query):
        """将自然语言转化为逻辑指令 (跨端增强版)"""
        q = query.lower()
        
        # 1. 请帖/邀请函生成 (Generative Content)
        if any(x in q for x in ["请帖", "邀请", "邀请函", "请贴"]):
            guest = self._extract_target(q, ["邀请", "给", "写"])
            if not guest: guest = "尊敬的贵宾"
            return [{"skill": "content_creator", "params": {"category": "invitation", "guest": guest}}]

        # 2. 午假/菜单生成 (Daily Intel)
        if "菜单" in q or ("今天" in q and "吃" in q):
            return [{"skill": "content_creator", "params": {"category": "menu"}}]

        # 3. 商务项目建立 (Project Architect)
        if any(x in q for x in ["新客户", "建立项目", "项目架构", "开案"]):
            name = self._extract_target(q, ["名为", "客户", "项目", "建立", "架构"])
            if not name: name = "Standard_Business_Project"
            return [{"skill": "project_architect", "params": {"name": name}}]

        # 4. 商业数据挖掘 (Data Mining)
        if any(x in q for x in ["提取", "汇总", "分析", "搜索", "寻找"]) and \
           any(x in q for x in ["邮件", "联系人", "发票", "金额", "钱", "元", "电话", "手机"]):
            data_type = "email"
            if any(x in q for x in ["发票", "金额", "钱", "元"]): data_type = "currency"
            if any(x in q for x in ["电话", "手机", "联系方式"]): data_type = "phone"
            return [{"skill": "data_miner", "params": {"data_type": data_type}}]

        # 5. 寻找/查找意图 (Cross-Platform Find)
        if any(x in q for x in ["找", "寻找", "查找", "哪里"]):
            target = self._extract_target(q, ["找", "寻找", "查找", "名为", "叫做"])
            path = self._extract_path(q)
            if target:
                if self.is_windows:
                    return [f"Get-ChildItem -Path {path} -Filter '*{target}*' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 5 -ExpandProperty FullName"]
                return [f"find {path} -name '*{target}*' -maxdepth 2 2>/dev/null | head -n 5"]

        # 6. 新建意图 (Cross-Platform Create)
        if any(x in q for x in ["新建", "建立", "创建", "生成"]):
            name = self._extract_target(q, ["名为", "叫做", "新建", "创建"])
            path = self._extract_path(q)
            if name:
                if "." not in name: name += ".txt"
                full_path = os.path.join(path, name)
                if self.is_windows:
                    return [f"New-Item -Path '{full_path}' -ItemType File -Force", f"Write-Output '已在 {path} 新建文件: {name}'"]
                return [f"touch {full_path}", f"echo '已在 {path} 新建文件: {name}'"]

        # 7. 系统状态/健康度 (Cross-Platform Stat)
        if "内存" in q or "进程" in q:
            if self.is_windows:
                return ["Get-Process | Sort-Object CPU -Descending | Select-Object -First 6 -Property Name, CPU"]
            return ["ps aux --sort=-%mem | head -n 6 | awk '{print $11 \" (MEM: \" $4 \"%)\"}'"]

        return []

    def _extract_target(self, q, keywords):
        """从句子中提取核心目标名称 (商务强化版)"""
        for kw in keywords:
            if kw in q:
                parts = q.split(kw)
                if len(parts) > 1:
                    target = parts[1].strip()
                    for filler in ["的架构", "架构", "的项目", "项目", "的文本", "文本", "的文件", "文件", "一个名为", "一个叫做", "的请帖内容", "的请帖", "的内容"]:
                        if target.startswith(filler):
                            target = target[len(filler):].strip()
                        if target.endswith(filler):
                            target = target[:-len(filler)].strip()
                    target = target.split(' ')[0].split('：')[0].split(':')[0]
                    return re.sub(r'[^\w\.-]', '', target) 
        return None

    def _extract_path(self, q):
        """从句子中提取路径关键词 (跨端适配)"""
        if "桌面" in q:
            if self.is_windows: return "$HOME\\Desktop"
            return "~/Desktop" if self.is_mac else "~/桌面"
        
        if "下载" in q or "download" in q:
            if self.is_windows: return "$HOME\\Downloads"
            return "~/Downloads"
            
        return "."
