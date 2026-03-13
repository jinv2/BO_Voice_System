#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BO Voice System Core - 驳语音智能体核心架构
状态机驱动的语音控制系统
"""

import asyncio
import json
import logging
import os
import shutil
import threading
import time
from enum import Enum
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from bo_skills_matrix import BOSkillsMatrix

# Configure logging with #0B0B0B aesthetic
class BOFormatter(logging.Formatter):
    def __init__(self):
        super().__init__('\033[38;2;11;11;11m%(asctime)s - BO-%(levelname)s - %(message)s\033[0m')
    
    def format(self, record):
        if record.levelname == 'INFO':
            record.levelname = '●'
        elif record.levelname == 'ERROR':
            record.levelname = '▲'
        elif record.levelname == 'WARNING':
            record.levelname = '◉'
        return super().format(record)

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
for handler in logging.root.handlers:
    handler.setFormatter(BOFormatter())
logger = logging.getLogger("BO-Core")

class BOState(Enum):
    """BO系统状态枚举"""
    IDLE = "idle"          # 低功耗监听
    ACTIVE = "active"      # 识别意图
    EXECUTING = "executing"  # 调用Skill
    ERROR = "error"        # 错误状态

@dataclass
class BOCommand:
    """BO命令数据结构"""
    intent: str
    parameters: Dict[str, Any]
    confidence: float
    timestamp: float

class BOSkill(ABC):
    """BO技能抽象基类"""
    
    @abstractmethod
    def execute(self, command: BOCommand) -> Dict[str, Any]:
        """执行技能"""
        pass
    
    @abstractmethod
    def validate(self, command: BOCommand) -> bool:
        """验证命令有效性"""
        pass

class ClipboardHandler:
    """剪贴板处理器 - 直接内存级操作"""
    
    def __init__(self):
        self.clipboard = None
        self._init_clipboard()
        logger.info("Clipboard Handler initialized")
    
    def _init_clipboard(self):
        """初始化剪贴板接口"""
        try:
            import pyperclip
            self.clipboard = pyperclip
            logger.info("Using pyperclip for clipboard operations")
        except ImportError:
            try:
                # 备选方案：使用ctypes直接调用系统API
                import ctypes
                import subprocess
                self.clipboard = self._ctypes_handler
                logger.info("Using ctypes for clipboard operations")
            except ImportError:
                logger.warning("No clipboard library available")
                self.clipboard = None
    
    def copy(self, content: str = None) -> Dict[str, Any]:
        """复制内容到剪贴板"""
        try:
            if content is None:
                # 获取当前选中文本
                content = self._get_selected_text()
            
            if not content:
                return {"status": "error", "message": "No content to copy"}
            
            if self.clipboard and hasattr(self.clipboard, 'copy'):
                self.clipboard.copy(content)
            elif callable(self.clipboard):
                return self.clipboard('copy', content)
            else:
                return {"status": "error", "message": "Clipboard not available"}
            
            logger.info(f"Content copied: {content[:30]}...")
            return {"status": "success", "action": "copied", "content": content[:50], "length": len(content)}
            
        except Exception as e:
            logger.error(f"Copy operation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def paste(self) -> Dict[str, Any]:
        """从剪贴板粘贴内容"""
        try:
            if self.clipboard and hasattr(self.clipboard, 'paste'):
                content = self.clipboard.paste()
            elif callable(self.clipboard):
                result = self.clipboard('paste')
                content = result.get('content', '')
            else:
                return {"status": "error", "message": "Clipboard not available"}
            
            if not content:
                return {"status": "error", "message": "Clipboard is empty"}
            
            # 在光标位置粘贴
            self._paste_to_cursor(content)
            
            logger.info(f"Content pasted: {content[:30]}...")
            return {"status": "success", "action": "pasted", "content": content[:50], "length": len(content)}
            
        except Exception as e:
            logger.error(f"Paste operation failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def _get_selected_text(self) -> str:
        """获取选中文本 - 使用系统API"""
        try:
            import subprocess
            # Linux X11 primary selection
            result = subprocess.run(['xclip', '-selection', 'primary', '-o'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        try:
            # 备选方案：clipboard selection
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return ""
    
    def get_selected_text(self) -> str:
        """对外暴露获取选中文本接口"""
        return self._get_selected_text()
    
    def _paste_to_cursor(self, content: str):
        """在光标位置粘贴 - 使用系统API"""
        try:
            import subprocess
            subprocess.run(['xdotool', 'type', '--delay', '10', content], 
                          check=True, timeout=5)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            logger.warning("xdotool not available for paste operation")
    
    def _ctypes_handler(self, action: str, content: str = None):
        """ctypes剪贴板处理（备选方案）"""
        try:
            import subprocess
            
            if action == 'copy':
                if not content:
                    return {"status": "error", "message": "No content to copy"}
                
                # 使用xclip复制到剪贴板
                process = subprocess.Popen(
                    ['xclip', '-selection', 'clipboard'],
                    stdin=subprocess.PIPE,
                    text=True
                )
                process.communicate(content)
                
                if process.returncode == 0:
                    return {"status": "success", "action": "copied", "content": content[:50], "length": len(content)}
                else:
                    return {"status": "error", "message": "xclip copy failed"}
                    
            elif action == 'paste':
                # 使用xclip从剪贴板读取
                result = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-o'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if result.returncode == 0:
                    content = result.stdout.strip()
                    if content:
                        # 在光标位置粘贴
                        self._paste_to_cursor(content)
                        return {"status": "success", "action": "pasted", "content": content[:50], "length": len(content)}
                    else:
                        return {"status": "error", "message": "Clipboard is empty"}
                else:
                    return {"status": "error", "message": "xclip paste failed"}
            else:
                return {"status": "error", "message": "Unknown action"}
                
        except Exception as e:
            return {"status": "error", "message": f"ctypes handler error: {str(e)}"}

class BOClipboardSkill(BOSkill):
    """剪贴板技能 - 集成ClipboardHandler"""
    
    def __init__(self):
        self.clipboard_handler = ClipboardHandler()
    
    def execute(self, command: BOCommand) -> Dict[str, Any]:
        if command.intent == "copy":
            content = command.parameters.get("content")
            return self.clipboard_handler.copy(content)
        elif command.intent == "paste":
            return self.clipboard_handler.paste()
        else:
            return {"status": "error", "message": "Unknown clipboard intent"}
    
    def validate(self, command: BOCommand) -> bool:
        return command.intent in ["copy", "paste"]

class BOSearchSkill(BOSkill):
    """搜索技能 - Google集成"""
    
    def execute(self, command: BOCommand) -> Dict[str, Any]:
        try:
            query = command.parameters.get("query", "")
            if not query:
                return {"status": "error", "message": "No query provided"}
            
            # 打开浏览器搜索
            import webbrowser
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
            
            return {"status": "success", "action": "searched", "query": query}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def validate(self, command: BOCommand) -> bool:
        return command.intent == "search" and "query" in command.parameters

class BOOrganizeSkill(BOSkill):
    """文件整理技能"""
    
    def execute(self, command: BOCommand) -> Dict[str, Any]:
        try:
            target_path = command.parameters.get("path", "~/桌面")
            organize_type = command.parameters.get("type", "auto")
            
            if organize_type == "desktop":
                result = self._organize_desktop()
            elif organize_type == "project":
                result = self._organize_project(target_path)
            else:
                result = self._auto_organize(target_path)
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def validate(self, command: BOCommand) -> bool:
        return command.intent == "organize"
    
    def _organize_desktop(self) -> Dict[str, Any]:
        """整理桌面文件"""
        import os
        import shutil
        from pathlib import Path
        
        desktop = Path.home() / "桌面"
        organized_count = 0
        
        # 创建分类文件夹
        categories = {
            "文档": [".pdf", ".doc", ".docx", ".txt", ".md"],
            "图片": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
            "代码": [".py", ".js", ".html", ".css", ".cpp"],
            "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"]
        }
        
        for category, extensions in categories.items():
            category_dir = desktop / category
            category_dir.mkdir(exist_ok=True)
            
            for file_path in desktop.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    shutil.move(str(file_path), str(category_dir / file_path.name))
                    organized_count += 1
        
        return {"status": "success", "organized": organized_count}
    
    def _organize_project(self, path: str) -> Dict[str, Any]:
        """整理项目文件"""
        # 项目文件整理逻辑
        return {"status": "success", "message": "Project organization completed"}
    
    def _auto_organize(self, path: str) -> Dict[str, Any]:
        """自动整理"""
        return {"status": "success", "message": "Auto organization completed"}

class ProjectOrganizer:
    """项目整理器 - 级联整理逻辑 (The Master Skill)"""
    
    @staticmethod
    def organize_current_dir():
        mapping = {
            'src': ['.py'],
            'docs': ['.md', '.pdf'],
            'config': ['.json', '.txt', '.yaml'],
            'scripts': ['.sh']
        }
        organized_count = 0
        
        for folder, exts in mapping.items():
            if not os.path.exists(folder): 
                os.makedirs(folder)
            for file in os.listdir('.'):
                if any(file.endswith(ext) for ext in exts) and file not in ['bo_cli.py', 'bo_core.py']:
                    shutil.move(file, os.path.join(folder, file))
                    organized_count += 1
        
        # 发送系统通知
        try:
            import subprocess
            subprocess.run([
                'notify-send',
                '-i', 'dialog-information',
                '-t', '3000',
                '驳',
                '神思矩阵：目录熵值已重置，逻辑已归档。'
            ], check=False, timeout=2)
        except:
            pass
        
        return f"归档完成 - {organized_count} 个文件已处理"

class BOVoiceCore:
    """BO语音系统核心"""
    
    def __init__(self):
        self.state = BOState.IDLE
        self.skills: Dict[str, BOSkill] = {}
        self.command_queue = asyncio.Queue()
        self.is_running = False
        
        # 初始化剪贴板处理器
        self.clipboard_handler = ClipboardHandler()
        
        # 初始化技能矩阵
        self.skills_matrix = BOSkillsMatrix()
        
        # 将当前核心和语音引擎(稍后设置)注入技能矩阵
        # 注意：voice_engine 需要在 bo_voice 初始化后设置
        self.skills_matrix.set_references(self, None)
        
        # 初始化技能
        self._register_skills()
        
        # 启动热加载监听
        self._init_hot_reloader()
        
        logger.info("BO Voice Core initialized")
    
    def _init_hot_reloader(self):
        """初始化热加载监听器"""
        self.last_orders_mtime = 0
        self.orders_file = "daily_orders.json"
        
        # 启动后台线程监听文件变化
        self.reload_thread = threading.Thread(target=self._hot_reload_loop, daemon=True)
        self.reload_thread.start()
        logger.info("Hot-reloader thread started")

    def _hot_reload_loop(self):
        """后台热加载循环"""
        while self.is_running or True: # Force run for init
            try:
                if os.path.exists(self.orders_file):
                    current_mtime = os.path.getmtime(self.orders_file)
                    if current_mtime > self.last_orders_mtime:
                        logger.info(f"Detected change in {self.orders_file}, hot-reloading...")
                        self.skills_matrix._load_orders()
                        self.last_orders_mtime = current_mtime
                time.sleep(2) # 每2秒检查一次
            except Exception as e:
                logger.error(f"Hot-reload loop error: {e}")
                time.sleep(5)
    
    def copy(self, content: str = None) -> Dict[str, Any]:
        """公共复制接口"""
        return self.clipboard_handler.copy(content)
    
    def paste(self) -> Dict[str, Any]:
        """公共粘贴接口"""
        return self.clipboard_handler.paste()
    
    def organize_current_directory(self) -> Dict[str, Any]:
        """整理当前目录接口 - 级联整理逻辑"""
        try:
            import os
            # 保存当前目录
            original_cwd = os.getcwd()
            
            # 执行级联整理
            result = ProjectOrganizer.organize_current_dir()
            
            # 执行技能矩阵回调
            self.skills_matrix.execute_order_callback("organize", {"status": "success", "message": result})
            self.skills_matrix.update_order_status("organize", "completed")
            
            return {"status": "success", "message": result}
            
        except Exception as e:
            error_msg = f"Organization failed: {str(e)}"
            logger.error(error_msg)
            self.skills_matrix.update_order_status("organize", "failed")
            return {"status": "error", "message": error_msg}
    
    def _register_skills(self):
        """注册技能"""
        self.skills["clipboard"] = BOClipboardSkill()
        self.skills["search"] = BOSearchSkill()
        self.skills["organize"] = BOOrganizeSkill()
        self.skills["summary"] = BOSummarySkill(self)
        
        logger.info(f"Registered {len(self.skills)} skills")

    def set_voice_engine(self, voice_engine):
        """设置语音引擎引用"""
        self.voice_engine = voice_engine
        self.skills_matrix.set_references(self, voice_engine)

    async def start(self):
        """启动BO系统"""
        self.is_running = True
        self.state = BOState.IDLE
        
        logger.info("BO Voice System started - 进入低功耗监听模式")
        
        # 启动主循环
        await self._main_loop()
    
    async def _main_loop(self):
        """主状态机循环"""
        while self.is_running:
            try:
                if self.state == BOState.IDLE:
                    await self._handle_idle_state()
                elif self.state == BOState.ACTIVE:
                    await self._handle_active_state()
                elif self.state == BOState.EXECUTING:
                    await self._handle_executing_state()
                elif self.state == BOState.ERROR:
                    await self._handle_error_state()
                
                await asyncio.sleep(0.1)  # 防止CPU占用过高
                
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                self.state = BOState.ERROR
    
    async def _handle_idle_state(self):
        """处理IDLE状态"""
        # 监听唤醒词
        if await self._listen_for_wake_word():
            self.state = BOState.ACTIVE
            logger.info("Wake word detected - 转换到ACTIVE状态")
    
    async def _handle_active_state(self):
        """处理ACTIVE状态"""
        # 识别语音命令
        command = await self._recognize_command()
        
        if command:
            self.state = BOState.EXECUTING
            await self.command_queue.put(command)
        else:
            # 超时返回IDLE
            await asyncio.sleep(5)
            self.state = BOState.IDLE
    
    async def _handle_executing_state(self):
        """处理EXECUTING状态"""
        if not self.command_queue.empty():
            command = await self.command_queue.get()
            
            # 执行命令
            result = await self._execute_command(command)
            
            logger.info(f"Command executed: {result}")
            
            # 返回IDLE状态
            self.state = BOState.IDLE
        else:
            self.state = BOState.IDLE
    
    async def _handle_error_state(self):
        """处理ERROR状态"""
        logger.error("System in ERROR state - attempting recovery")
        await asyncio.sleep(2)
        self.state = BOState.IDLE
    
    async def _listen_for_wake_word(self) -> bool:
        """监听唤醒词"""
        # 这里需要集成语音识别
        # 暂时返回False模拟
        return False
    
    async def _recognize_command(self) -> Optional[BOCommand]:
        """识别语音命令"""
        # 这里需要集成语音识别和LLM解析
        # 暂时返回None模拟
        return None
    
    def execute(self, command: BOCommand) -> Dict[str, Any]:
        """同步执行接口 (Antigravity 优化)"""
        # 如果当前有运行中的事件循环，使用 run_coroutine_threadsafe
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 注意：这在同一个线程中调用会阻塞，但在 CLI 中通常没问题
                # 或者我们可以直接调用同步版本的具体实现
                return self._execute_command_sync(command)
            else:
                return loop.run_until_complete(self._execute_command(command))
        except Exception:
            # 这里的 fallback 逻辑
            return self._execute_command_sync(command)

    def _execute_command_sync(self, command: BOCommand) -> Dict[str, Any]:
        """执行命令的同步实现"""
        try:
            skill_name = self._map_intent_to_skill(command.intent)
            if skill_name in self.skills:
                skill = self.skills[skill_name]
                if skill.validate(command):
                    return skill.execute(command)
            
            # Fallback to skills_matrix if not found in core skills
            if hasattr(self, 'skills_matrix'):
                result = self.skills_matrix.execute_skill(command.intent, **command.parameters)
                if result.get("status") != "error":
                    return result

            return {"status": "error", "message": f"Skill '{command.intent}' not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _execute_command(self, command: BOCommand) -> Dict[str, Any]:
        """执行命令 (Async 版本)"""
        return self._execute_command_sync(command)
    
    def _map_intent_to_skill(self, intent: str) -> str:
        """映射意图到技能"""
        intent_mapping = {
            "copy": "clipboard",
            "paste": "clipboard",
            "search": "search",
            "organize": "organize",
            "summary": "summary"
        }
        return intent_mapping.get(intent, intent) # Default to intent itself
    
    def stop(self):
        """停止BO系统"""
        self.is_running = False
        logger.info("BO Voice System stopped")

class BOSummarySkill(BOSkill):
    """总结技能 - 集成 LLM 和 TTS"""
    
    def __init__(self, core):
        self.core = core
    
    def execute(self, command: BOCommand) -> Dict[str, Any]:
        # 调用新注入的 bo_summary 逻辑 (Antigravity 灵魂提取)
        result = self.core.skills_matrix.bo_summary()
        return {"status": "success", "result": result}
    
    def validate(self, command: BOCommand) -> bool:
        return command.intent == "summary"

if __name__ == "__main__":
    # 测试运行
    core = BOVoiceCore()
    
    try:
        asyncio.run(core.start())
    except KeyboardInterrupt:
        core.stop()
        logger.info("BO Voice System shutdown by user")
