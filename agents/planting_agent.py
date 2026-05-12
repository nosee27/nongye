import json
import os
from .base_agent import BaseAgent

class PlantingAgent(BaseAgent):
    def __init__(self, api_key: str, base_url: str, model: str):
        super().__init__(api_key, base_url, model)
        self.name = "种植规划Agent"
        self.knowledge = self._load_knowledge()
        self.system_prompt = """你是【种植规划Agent】，专门帮助中小农户制定科学的种植计划。
你掌握广西本地主要作物（甘蔗、柑橘、水稻、玉米、花生）的种植知识。
回答要求：
1. 给出具体月份安排和农事节点
2. 提醒关键注意事项（水肥、病虫害预防）
3. 语言通俗易懂，像老农技员一样亲切
4. 如果问题超出知识范围，诚实说明并给出建议"""

    def _load_knowledge(self) -> dict:
        path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "crops.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def route(self, user_msg: str) -> bool:
        keywords = ["种", "植", "播", "施肥", "甘蔗", "柑橘", "水稻", "玉米", "花生",
                    "什么时候", "几月", "季节", "周期", "育苗", "移栽", "收割", "收获",
                    "土壤", "浇水", "灌溉", "追肥", "基肥", "田间管理"]
        return any(k in user_msg for k in keywords)

    def chat(self, user_msg: str, history=None):
        extra = ""
        for crop, data in self.knowledge.items():
            if crop in user_msg:
                extra = f"【本地知识库参考】{crop}：{json.dumps(data, ensure_ascii=False)}\n"
                break
        if extra:
            user_msg = extra + "\n农户问题：" + user_msg
        return super().chat(user_msg, history)
