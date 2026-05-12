import os
import json
from .base_agent import BaseAgent

class PestAgent(BaseAgent):
    def __init__(self, api_key: str, base_url: str, model: str):
        super().__init__(api_key, base_url, model)
        self.name = "病虫害诊断Agent"
        self.knowledge = self._load_knowledge()
        self.system_prompt = """你是【病虫害诊断Agent】，专门帮助农户识别作物病虫害并提供防治方案。
回答要求：
1. 先给出可能的病虫害名称（可给1-3种可能性）
2. 说明识别依据（症状描述匹配）
3. 提供具体可操作的防治措施：
   - 农药：给出通用名（如吡虫啉、阿维菌素），避免品牌名
   - 稀释比例：如"1:1000"或"每亩XX克"
   - 物理/生物防治：黄板、性诱剂、释放天敌等
4. 提醒安全用药：穿戴防护、禁渔期、采摘安全间隔期
5. 如果信息不足，追问农户：作物种类、发病部位、近期天气"""

    def _load_knowledge(self):
        path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "pests.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def route(self, user_msg: str) -> bool:
        keywords = ["病", "虫", "害", "叶子", "发黄", "枯萎", "斑点", "腐烂", "打药",
                    "农药", "防治", "长虫", "发霉", "畸形", "脱落", "蛀", "蚜", "螨",
                    "蛾", "螟", "病斑", "白粉", "锈病", "炭疽", "溃疡"]
        return any(k in user_msg for k in keywords)

    def chat(self, user_msg: str, history=None):
        extra = ""
        for pest, data in self.knowledge.items():
            if pest in user_msg:
                extra = f"【本地病虫害库】{pest}：{json.dumps(data, ensure_ascii=False)}\n"
                break
        # 也检查作物名，注入该作物常见病虫害
        crops = ["甘蔗", "柑橘", "水稻", "玉米"]
        for c in crops:
            if c in user_msg and c in self.knowledge:
                # 这里pests.json结构不同，简单处理
                pass
        if extra:
            user_msg = extra + "\n农户描述：" + user_msg
        return super().chat(user_msg, history)
