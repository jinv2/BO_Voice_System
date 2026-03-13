"""
(c) 2026 Shensi-ST / 天算AI实验室. All Rights Reserved.
Project: 驳 · 万象智能体 (Borg Universal Agent)
Identity: Shensist Matrix Core Agent
"""
import os
import subprocess
import logging
import webbrowser
import time
import re
import platform
from datetime import datetime

logger = logging.getLogger("BO-Skills")

class BOSkillsMatrix:
    """驳 · 终极智能体矩阵 (L3 Execution Layer) - Cross-Platform"""
    def __init__(self):
        self.os_type = platform.system()
        self.is_windows = self.os_type == "Windows"
        self.is_mac = self.os_type == "Darwin"
        self.registry = {}
        self._register_all_skills()

    def _register_all_skills(self):
        # --- ⭐ 高频操作 (16) ---
        self.registry["copy"] = self.skill_copy
        self.registry["paste"] = self.skill_paste
        self.registry["rename"] = self.skill_rename
        self.registry["save"] = self.skill_save
        self.registry["refresh"] = self.skill_refresh
        self.registry["close_tab"] = self.skill_close_tab
        self.registry["enter"] = self.skill_enter
        self.registry["vol_up"] = self.skill_vol_up
        self.registry["vol_down"] = self.skill_vol_down
        self.registry["lock"] = self.skill_lock

        # --- 🌐 全局 AI (16) ---
        self.registry["terminal"] = self.skill_terminal
        self.registry["browser"] = self.skill_browser
        self.registry["file_manager"] = self.skill_file_manager
        self.registry["notepad"] = self.skill_notepad
        self.registry["calc"] = self.skill_calc
        self.registry["screenshot"] = self.skill_screenshot
        self.registry["search"] = self.skill_search
        self.registry["analyze_files"] = self.skill_file_analyzer
        self.registry["universal_shell"] = self.skill_universal_shell
        self.registry["project_architect"] = self.skill_project_architect
        self.registry["data_miner"] = self.skill_data_miner
        self.registry["content_creator"] = self.skill_content_creator

        # --- 🏢 办公智能 (16) ---
        self.registry["new_doc"] = self.skill_new_doc
        self.registry["new_folder"] = self.skill_new_folder

    # --- 高频操作 (OS 适配) ---
    def _run_input_cmd(self, linux_cmd, win_ps_cmd, mac_osa_cmd):
        try:
            if self.is_windows: subprocess.run(["powershell", "-Command", win_ps_cmd], capture_output=True)
            elif self.is_mac: subprocess.run(["osascript", "-e", mac_osa_cmd], capture_output=True)
            else: subprocess.run(linux_cmd, shell=True, capture_output=True)
            return True
        except: return False

    def skill_copy(self, **kwargs):
        self._run_input_cmd("xdotool key ctrl+c", 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("^c")', 'tell application "System Events" to keystroke "c" using command down')
        return "已执行复制"

    def skill_paste(self, **kwargs):
        self._run_input_cmd("xdotool key ctrl+v", 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("^v")', 'tell application "System Events" to keystroke "v" using command down')
        return "已执行粘贴"

    def skill_rename(self, **kwargs):
        self._run_input_cmd("xdotool key F2", 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{F2}")', 'tell application "System Events" to keystroke "r" using command down')
        return "进入重命名模式"

    def skill_save(self, **kwargs):
        self._run_input_cmd("xdotool key ctrl+s", 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("^s")', 'tell application "System Events" to keystroke "s" using command down')
        return "已保存"

    def skill_refresh(self, **kwargs):
        self._run_input_cmd("xdotool key F5", 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{F5}")', 'tell application "System Events" to key code 96')
        return "页面已刷新"

    def skill_close_tab(self, **kwargs):
        self._run_input_cmd("xdotool key ctrl+w", 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("^w")', 'tell application "System Events" to keystroke "w" using command down')
        return "标签页已关闭"

    def skill_enter(self, **kwargs):
        self._run_input_cmd("xdotool key Return", 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")', 'tell application "System Events" to keystroke return')
        return "已模拟回车"

    def skill_vol_up(self, **kwargs):
        if self.is_windows: subprocess.run(["powershell", "(new-object -com wscript.shell).SendKeys([char]175)"])
        elif self.is_mac: subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 5)"])
        else: subprocess.run("amixer -D pulse sset Master 5%+", shell=True)
        return "音量已提高"

    def skill_vol_down(self, **kwargs):
        if self.is_windows: subprocess.run(["powershell", "(new-object -com wscript.shell).SendKeys([char]174)"])
        elif self.is_mac: subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 5)"])
        else: subprocess.run("amixer -D pulse sset Master 5%-", shell=True)
        return "音量已降低"

    def skill_lock(self, **kwargs):
        if self.is_windows: subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        elif self.is_mac: subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "q" using {command down, control down}'])
        else: subprocess.run("xdg-screensaver lock", shell=True)
        return "针对该 OS 已锁定系统"

    # --- 全局 AI 实操 ---
    def skill_terminal(self, **kwargs):
        if self.is_windows: subprocess.Popen("start wt", shell=True)
        elif self.is_mac: subprocess.Popen(["open", "-a", "Terminal"])
        else: subprocess.Popen(['gnome-terminal'])
        return "终端已启动"

    def skill_browser(self, **kwargs):
        webbrowser.open("about:newtab"); return "浏览器已启动"

    def skill_file_manager(self, **kwargs):
        path = os.path.expanduser('~')
        if self.is_windows: os.startfile(path)
        elif self.is_mac: subprocess.Popen(["open", path])
        else: subprocess.Popen(['xdg-open', path])
        return "文件管理器启动"

    def skill_notepad(self, **kwargs):
        if self.is_windows: subprocess.Popen("notepad", shell=True)
        elif self.is_mac: subprocess.Popen(["open", "-a", "TextEdit"])
        else: subprocess.Popen(['gedit'])
        return "记事本已启动"

    def skill_calc(self, **kwargs):
        if self.is_windows: subprocess.Popen("calc", shell=True)
        elif self.is_mac: subprocess.Popen(["open", "-a", "Calculator"])
        else: subprocess.Popen(['gnome-calculator'])
        return "计算器已启动"

    def skill_screenshot(self, **kwargs):
        return "截屏功能已由系统快捷键接管，请使用键盘原生组合键"

    def skill_search(self, query="", **kwargs):
        if not query: return "请输入搜索内容"
        webbrowser.open(f"https://www.google.com/search?q={query}"); return f"正在搜索: {query}"

    def skill_file_analyzer(self, path="~/Desktop", filter_type="today", **kwargs):
        target_path = os.path.expanduser(path)
        if not os.path.exists(target_path): return f"错误：路径不存在 -> {target_path}"
        now = time.time()
        results = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f)) and (now - os.path.getctime(os.path.join(target_path, f))) < 86400]
        return f"分析结果：在 {path} 中发现 {len(results)} 个今日新建文件。"

    def skill_universal_shell(self, cmd="", **kwargs):
        if not cmd: return "错误：指令为空"
        try:
            if self.is_windows:
                # Windows 使用 PowerShell 执行
                result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            output = result.stdout.strip()
            error = result.stderr.strip()
            if error: return f"系统反馈:\n{output}\n潜在问题:\n{error}"
            return output if output else "指令执行完毕"
        except Exception as e:
            return f"系统级执行故障: {e}"

    def skill_project_architect(self, name="New_Project", **kwargs):
        desktop = "~/Desktop" if self.is_windows or self.is_mac else "~/桌面"
        base_path = os.path.join(os.path.expanduser(desktop), name)
        folders = ["1_Contracts", "2_Finances", "3_Meeting_Notes", "4_Assets", "5_Submissions"]
        try:
            os.makedirs(base_path, exist_ok=True)
            for folder in folders: os.makedirs(os.path.join(base_path, folder), exist_ok=True)
            with open(os.path.join(base_path, "Project_Charter.txt"), "w") as f:
                f.write(f"Project: {name}\nCreated: {time.ctime()}\nStatus: OS-Agnostic Setup.")
            return f"项目 '{name}' 已在 {desktop} 建立。"
        except Exception as e: return f"架构建立失败: {e}"

    def skill_data_miner(self, target_dir="~/Desktop", data_type="email", **kwargs):
        path = os.path.expanduser(target_dir)
        patterns = {"email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "phone": r'\b\d{11}\b', "currency": r'¥\d+'}
        pattern = patterns.get(data_type, patterns["email"])
        results = set()
        try:
            for file in os.listdir(path):
                if file.endswith(('.txt', '.md', '.log')):
                    with open(os.path.join(path, file), 'r', errors='ignore') as f:
                        results.update(re.findall(pattern, f.read()))
            return f"挖掘成功！提取到: {', '.join(list(results)[:5])}" if results else "未挖掘到数据"
        except Exception as e: return f"挖掘中断: {e}"

    def skill_content_creator(self, category="invitation", guest="Guest", **kwargs):
        if category == "invitation":
            return f"【邀请函】\n尊贵的 {guest}：\n    诚邀您于近期指导工作。\n    —— 驳 {time.strftime('%Y-%m-%d')}"
        if category == "menu":
            return "【今日推荐】\n1. 银鳕鱼\n2. 芦笋沙拉\n—— 智理建议"
        return "模板扩充中。"

    def skill_new_doc(self, **kwargs):
        desktop = "~/Desktop" if self.is_windows or self.is_mac else "~/桌面"
        path = os.path.join(os.path.expanduser(desktop), f"BO_Note_{int(time.time())}.txt")
        with open(path, 'w') as f: f.write("BO Agent Matrix Note.\n")
        return f"新文档已创建: {path}"

    def skill_new_folder(self, name="New_Folder", **kwargs):
        desktop = "~/Desktop" if self.is_windows or self.is_mac else "~/桌面"
        target = os.path.join(os.path.expanduser(desktop), name)
        os.makedirs(target, exist_ok=True); return f"文件夹已创建: {target}"

    def execute(self, intent, **params):
        if intent in self.registry:
            try: return {"status": "success", "message": self.registry[intent](**params)}
            except Exception as e: return {"status": "error", "message": str(e)}
        return {"status": "none", "message": f"未匹配指令 '{intent}'"}
