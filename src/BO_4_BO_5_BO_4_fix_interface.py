import asyncio
from src.bo_core import BOVoiceCore

# 为 BOVoiceCore 动态注入同步兼容接口
def sync_execute_wrapper(self, intent, args):
    from src.bo_skills_matrix import bo_web_search, bo_summary
    if intent == "search":
        return bo_web_search(args.get('query', ''))
    elif intent == "summary":
        return bo_summary()
    return {"status": "unknown_intent"}

# 物理注入（手动或通过脚本对齐）
