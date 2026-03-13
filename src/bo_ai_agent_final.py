#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(c) 2026 Shensi-ST / 天算AI实验室. All Rights Reserved.
Project: 驳 · 万象智能体 (Borg Universal Agent)
Identity: Shensist Matrix Core Agent
"""
"""
BO AI Agent Final - 驳智能体核心
实时意识流记录和动态看板管理
"""

import json
import logging
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Apply BO aesthetic formatting
from bo_core import BOFormatter

bo_logger = logging.getLogger("BO-AIAgent")
bo_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(BOFormatter())
bo_logger.addHandler(handler)
logger = bo_logger

class BOAIAgent:
    """驳AI智能体 - 实时意识流记录器"""
    
    def __init__(self, orders_file: str = "daily_orders.json"):
        self.orders_file = orders_file
        self.consciousness_stream = []
        self.skill_execution_history = []
        
        self._load_orders()
        logger.info("BO AI Agent initialized - 实时意识流在线")
    
    def _load_orders(self):
        """加载订单配置"""
        try:
            orders_path = Path(self.orders_file)
            if orders_path.exists():
                with open(orders_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.active_orders = data.get("active_orders", [])
                self.skills_matrix = data.get("skills_matrix", {})
            else:
                self.active_orders = []
                self.skills_matrix = {}
        except Exception as e:
            logger.error(f"Failed to load orders: {e}")
            self.active_orders = []
            self.skills_matrix = {}
    
    def record_skill_execution(self, skill_name: str, result: Dict[str, Any], context: Dict[str, Any] = None):
        """记录技能执行 - 实时意识流"""
        try:
            timestamp = datetime.now()
            
            # 创建意识流记录
            consciousness_entry = {
                "timestamp": timestamp.isoformat(),
                "skill": skill_name,
                "result": result,
                "context": context or {},
                "status": result.get("status", "unknown"),
                "duration": context.get("duration", 0) if context else 0,
                "user_intent": context.get("user_intent", "") if context else ""
            }
            
            # 添加到意识流
            self.consciousness_stream.append(consciousness_entry)
            
            # 保持最近100条记录
            if len(self.consciousness_stream) > 100:
                self.consciousness_stream = self.consciousness_stream[-100:]
            
            # 更新daily_orders.json
            self._update_daily_orders(skill_name, result, timestamp)
            
            logger.info(f"Consciousness stream updated: {skill_name} -> {result.get('status')}")
            
        except Exception as e:
            logger.error(f"Failed to record skill execution: {e}")
    
    def _update_daily_orders(self, skill_name: str, result: Dict[str, Any], timestamp: datetime):
        """更新daily_orders.json - 实时意识流记录"""
        try:
            # 读取现有配置
            data = self._read_orders_file()
            
            # 更新对应订单的状态
            for order in data.get("active_orders", []):
                if order.get("intent") == skill_name:
                    order["last_run"] = timestamp.isoformat()
                    order["status"] = result.get("status", "unknown")
                    order["last_result"] = {
                        "message": result.get("message", ""),
                        "success": result.get("status") == "success"
                    }
                    break
            
            # 添加意识流摘要
            consciousness_summary = {
                "last_skill": skill_name,
                "last_execution": timestamp.isoformat(),
                "total_executions": len(self.consciousness_stream),
                "recent_success_rate": self._calculate_success_rate(),
                "active_skills": list(set(entry["skill"] for entry in self.consciousness_stream[-10:]))
            }
            
            data["consciousness_summary"] = consciousness_summary
            data["last_updated"] = timestamp.isoformat()
            
            # 保存更新
            self._save_orders_file(data)
            
        except Exception as e:
            logger.error(f"Failed to update daily orders: {e}")
    
    def _read_orders_file(self) -> Dict[str, Any]:
        """读取订单文件"""
        try:
            if os.path.exists(self.orders_file):
                with open(self.orders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    "project": "BO_Voice_System",
                    "version": "1.0.0",
                    "skills_matrix": self.skills_matrix,
                    "active_orders": self.active_orders
                }
        except Exception as e:
            logger.error(f"Failed to read orders file: {e}")
            return {}
    
    def _save_orders_file(self, data: Dict[str, Any]):
        """保存订单文件"""
        try:
            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save orders file: {e}")
    
    def _calculate_success_rate(self) -> float:
        """计算最近成功率"""
        if not self.consciousness_stream:
            return 0.0
        
        recent_entries = self.consciousness_stream[-20:]  # 最近20次
        success_count = sum(1 for entry in recent_entries if entry.get("status") == "success")
        
        return (success_count / len(recent_entries)) * 100 if recent_entries else 0.0
    
    def get_consciousness_summary(self) -> Dict[str, Any]:
        """获取意识流摘要"""
        if not self.consciousness_stream:
            return {"status": "empty", "message": "No consciousness data"}
        
        recent_entries = self.consciousness_stream[-10:]
        
        return {
            "total_executions": len(self.consciousness_stream),
            "recent_executions": len(recent_entries),
            "success_rate": self._calculate_success_rate(),
            "last_skill": self.consciousness_stream[-1]["skill"],
            "last_execution": self.consciousness_stream[-1]["timestamp"],
            "active_skills": list(set(entry["skill"] for entry in recent_entries)),
            "recent_timeline": [
                {
                    "time": entry["timestamp"],
                    "skill": entry["skill"],
                    "status": entry["status"]
                }
                for entry in recent_entries
            ]
        }
    
    def get_skill_statistics(self, skill_name: str) -> Dict[str, Any]:
        """获取技能统计"""
        skill_entries = [entry for entry in self.consciousness_stream if entry["skill"] == skill_name]
        
        if not skill_entries:
            return {"status": "not_found", "skill": skill_name}
        
        success_count = sum(1 for entry in skill_entries if entry.get("status") == "success")
        
        return {
            "skill": skill_name,
            "total_executions": len(skill_entries),
            "success_count": success_count,
            "success_rate": (success_count / len(skill_entries)) * 100,
            "first_execution": skill_entries[0]["timestamp"],
            "last_execution": skill_entries[-1]["timestamp"],
            "average_duration": sum(entry.get("duration", 0) for entry in skill_entries) / len(skill_entries)
        }
    
    def export_consciousness(self, format: str = "json") -> str:
        """导出意识流数据"""
        try:
            if format == "json":
                return json.dumps(self.consciousness_stream, ensure_ascii=False, indent=2)
            elif format == "summary":
                return json.dumps(self.get_consciousness_summary(), ensure_ascii=False, indent=2)
            else:
                return "Unsupported format"
        except Exception as e:
            logger.error(f"Failed to export consciousness: {e}")
            return "{}"
    
    def clear_consciousness(self):
        """清空意识流"""
        self.consciousness_stream.clear()
        logger.info("Consciousness stream cleared")
    
    def get_daily_report(self) -> Dict[str, Any]:
        """生成日报"""
        today = datetime.now().date().isoformat()
        today_entries = [
            entry for entry in self.consciousness_stream 
            if entry["timestamp"].startswith(today)
        ]
        
        if not today_entries:
            return {"date": today, "status": "no_activity"}
        
        skills_used = set(entry["skill"] for entry in today_entries)
        success_count = sum(1 for entry in today_entries if entry.get("status") == "success")
        
        return {
            "date": today,
            "total_executions": len(today_entries),
            "unique_skills": len(skills_used),
            "success_rate": (success_count / len(today_entries)) * 100,
            "skills_used": list(skills_used),
            "first_activity": today_entries[0]["timestamp"],
            "last_activity": today_entries[-1]["timestamp"],
            "hourly_distribution": self._calculate_hourly_distribution(today_entries)
        }
    
    def _calculate_hourly_distribution(self, entries: list) -> Dict[str, int]:
        """计算小时分布"""
        distribution = {}
        for entry in entries:
            hour = entry["timestamp"][11:13]  # 提取小时
            distribution[hour] = distribution.get(hour, 0) + 1
        return distribution

# 全局AI智能体实例
ai_agent = BOAIAgent()

# 技能执行装饰器
def record_skill_execution(skill_name: str):
    """装饰器：自动记录技能执行"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                
                # 记录执行
                context = {
                    "duration": (datetime.now() - start_time).total_seconds(),
                    "user_intent": kwargs.get("user_intent", ""),
                    "parameters": kwargs
                }
                
                ai_agent.record_skill_execution(skill_name, result, context)
                
                return result
                
            except Exception as e:
                # 记录错误
                error_result = {"status": "error", "message": str(e)}
                context = {
                    "duration": (datetime.now() - start_time).total_seconds(),
                    "user_intent": kwargs.get("user_intent", ""),
                    "error": str(e)
                }
                
                ai_agent.record_skill_execution(skill_name, error_result, context)
                
                raise
                
        return wrapper
    return decorator

# 测试代码
if __name__ == "__main__":
    print("🧠 测试 BO AI Agent")
    
    # 模拟技能执行
    test_results = [
        {"status": "success", "message": "Volume set to 50%"},
        {"status": "success", "message": "Screen locked"},
        {"status": "error", "message": "Failed to organize"},
        {"status": "success", "message": "Files organized"}
    ]
    
    for i, result in enumerate(test_results):
        skill_name = ["volume_control", "screen_lock", "organize", "organize"][i]
        ai_agent.record_skill_execution(skill_name, result, {"user_intent": f"test_{i}"})
    
    print("\n📊 意识流摘要:")
    summary = ai_agent.get_consciousness_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    print("\n📈 技能统计:")
    stats = ai_agent.get_skill_statistics("organize")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    print("\n📅 今日报告:")
    daily = ai_agent.get_daily_report()
    print(json.dumps(daily, ensure_ascii=False, indent=2))