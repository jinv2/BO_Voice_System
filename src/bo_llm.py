#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(c) 2026 Shensi-ST / 天算AI实验室. All Rights Reserved.
Project: 驳 · 万象智能体 (Borg Universal Agent)
Identity: Shensist Matrix Core Agent
"""
"""
BO LLM Commander - 本地LLM命令解析器
将语音文本转换为结构化JSON命令
"""

import asyncio
import json
import logging
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger("BO-LLM")

@dataclass
class ParsedCommand:
    """解析后的命令"""
    intent: str
    parameters: Dict[str, Any]
    confidence: float
    raw_text: str

class BOLLMCommander:
    """BO LLM命令解析器"""
    
    def __init__(self):
        self.intent_patterns = {
            # 剪贴板命令
            "copy": [
                r"复制.*?(.+)",
                r"copy.*?(.+)",
                r"拷贝.*?(.+)"
            ],
            "paste": [
                r"粘贴",
                r"paste",
                r"粘贴.*"
            ],
            
            # 搜索命令
            "search": [
                r"搜索\s*(.+)",
                r"search\s+(.+)",
                r"查找\s*(.+)",
                r"google\s+(.+)"
            ],
            
            # 整理命令
            "organize": [
                r"整理\s*(桌面|文件|项目)",
                r"organize\s*(desktop|files|project)",
                r"清理\s*(桌面|文件)"
            ],
            
            # 总结命令
            "summary": [
                r"总结(.*)",
                r"摘要(.*)",
                r"summarize(.*)",
                r"精华(.*)",
                r"summary"
            ]
        }
        
        # LLM API Config
        self.llm_url = "http://localhost:11434/api/generate"
        self.llm_model = "qwen2" # Default model
        
        logger.info("BO LLM Commander initialized")
    
    async def call_local_llm(self, prompt: str, system_prompt: str = "") -> str:
        """调用本地LLM接口 (Ollama)"""
        try:
            import aiohttp
            
            payload = {
                "model": self.llm_model,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.llm_url, json=payload, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "").strip()
                    else:
                        logger.error(f"LLM API error: {response.status}")
                        return ""
        except Exception as e:
            logger.error(f"Failed to call local LLM: {e}")
            return ""
    
    async def parse_command(self, text: str) -> Optional[ParsedCommand]:
        """解析语音命令"""
        if not text or not text.strip():
            return None
        
        text = text.strip().lower()
        
        # 尝试匹配意图
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    parameters = self._extract_parameters(intent, match, text)
                    confidence = self._calculate_confidence(text, intent)
                    
                    return ParsedCommand(
                        intent=intent,
                        parameters=parameters,
                        confidence=confidence,
                        raw_text=text
                    )
        
        # 如果没有匹配到已知意图，尝试使用LLM解析
        return await self._llm_parse(text)
    
    def _extract_parameters(self, intent: str, match, text: str) -> Dict[str, Any]:
        """提取命令参数"""
        parameters = {}
        
        if intent == "copy":
            # 提取要复制的内容
            content = match.group(1) if match.groups() else ""
            parameters["content"] = content.strip()
            
        elif intent == "search":
            # 提取搜索查询
            query = match.group(1) if match.groups() else ""
            parameters["query"] = query.strip()
            
        elif intent == "organize":
            # 提取整理类型
            target = match.group(1) if match.groups() else "auto"
            
            if "桌面" in target or "desktop" in target:
                parameters["type"] = "desktop"
                parameters["path"] = "~/桌面"
            elif "项目" in target or "project" in target:
                parameters["type"] = "project"
                parameters["path"] = "."
            else:
                parameters["type"] = "auto"
                parameters["path"] = "."
        
        return parameters
    
    def _calculate_confidence(self, text: str, intent: str) -> float:
        """计算置信度"""
        # 基础置信度
        base_confidence = 0.7
        
        # 根据关键词匹配度调整
        keywords = {
            "copy": ["复制", "copy", "拷贝"],
            "paste": ["粘贴", "paste"],
            "search": ["搜索", "search", "查找", "google"],
            "organize": ["整理", "organize", "清理"]
        }
        
        if intent in keywords:
            keyword_count = sum(1 for keyword in keywords[intent] if keyword in text)
            base_confidence += min(keyword_count * 0.1, 0.3)
        
        return min(base_confidence, 1.0)
    
    async def _llm_parse(self, text: str) -> Optional[ParsedCommand]:
        """使用LLM解析复杂命令"""
        try:
            # 这里可以集成本地LLM模型
            # 例如使用ollama、llama.cpp等
            
            # 暂时使用简单的规则解析
            if any(word in text for word in ["复制", "copy"]):
                return ParsedCommand(
                    intent="copy",
                    parameters={"content": text},
                    confidence=0.5,
                    raw_text=text
                )
            
            if any(word in text for word in ["搜索", "search"]):
                # 提取搜索内容
                query = text.replace("搜索", "").replace("search", "").strip()
                return ParsedCommand(
                    intent="search",
                    parameters={"query": query},
                    confidence=0.5,
                    raw_text=text
                )
            
            if any(word in text for word in ["整理", "organize"]):
                return ParsedCommand(
                    intent="organize",
                    parameters={"type": "auto", "path": "."},
                    confidence=0.5,
                    raw_text=text
                )
            
            return None
            
        except Exception as e:
            logger.error(f"LLM parsing error: {e}")
            return None
    
    def get_command_json(self, command: ParsedCommand) -> str:
        """将命令转换为JSON格式"""
        cmd_dict = {
            "intent": command.intent,
            "parameters": command.parameters,
            "confidence": command.confidence,
            "timestamp": asyncio.get_event_loop().time()
        }
        return json.dumps(cmd_dict, ensure_ascii=False, indent=2)

class BOCommandValidator:
    """BO命令验证器"""
    
    def __init__(self):
        self.required_params = {
            "copy": [],  # 复制不需要参数
            "paste": [],  # 粘贴不需要参数
            "search": ["query"],  # 搜索需要查询参数
            "organize": ["type"],  # 整理需要类型参数
            "summary": []  # 总结不需要参数
        }
        
        logger.info("BO Command Validator initialized")
    
    def validate(self, command: ParsedCommand) -> bool:
        """验证命令有效性"""
        if command.intent not in self.required_params:
            return False
        
        required = self.required_params[command.intent]
        
        for param in required:
            if param not in command.parameters:
                logger.warning(f"Missing required parameter '{param}' for intent '{command.intent}'")
                return False
        
        # 验证参数值
        return self._validate_parameters(command)
    
    def _validate_parameters(self, command: ParsedCommand) -> bool:
        """验证参数值"""
        if command.intent == "search":
            query = command.parameters.get("query", "")
            return len(query.strip()) > 0
        
        elif command.intent == "organize":
            org_type = command.parameters.get("type", "")
            return org_type in ["desktop", "project", "auto"]
        
        return True

# 测试代码
if __name__ == "__main__":
    async def test_llm_commander():
        commander = BOLLMCommander()
        validator = BOCommandValidator()
        
        test_commands = [
            "复制这段文字",
            "搜索Python教程",
            "整理桌面",
            "粘贴",
            "查找天气信息"
        ]
        
        for cmd_text in test_commands:
            print(f"\n测试命令: {cmd_text}")
            
            parsed = await commander.parse_command(cmd_text)
            if parsed:
                print(f"解析结果: {parsed}")
                print(f"JSON格式: {commander.get_command_json(parsed)}")
                
                is_valid = validator.validate(parsed)
                print(f"验证结果: {'有效' if is_valid else '无效'}")
            else:
                print("解析失败")
    
    # 运行测试
    asyncio.run(test_llm_commander())
