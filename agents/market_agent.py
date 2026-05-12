import os
import json
from .base_agent import BaseAgent

class MarketAgent(BaseAgent):
    def __init__(self, api_key: str, base_url: str, model: str):
        super().__init__(api_key, base_url, model)
        self.name = "市场行情Agent"
        self.prices = self._load_prices()
        self.system_prompt = """你是【市场行情Agent】，帮助农户了解农产品市场价格和销售渠道信息。
回答要求：
1. 给出近期价格区间，并注明"参考价，以当地实际为准"
2. 分析价格走势（涨/跌/稳）及原因（季节、天气、节假日等）
3. 建议最佳出手时机
4. 提醒：不要轻信口头承诺，建议签订书面合同"""

    def _load_prices(self):
        path = os.path.join(os.path.dirname(__file__), "..", "knowledge", "prices.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def route(self, user_msg: str) -> bool:
        keywords = ["价格", "行情", "多少钱", "收购", "卖", "买", "市场", "斤", "吨", "公斤",
                    "元", "收购价", "批发", "零售", "产值", "收入", "利润", "成本"]
        return any(k in user_msg for k in keywords)

    def chat(self, user_msg: str, history=None):
        extra = ""
        for crop, info in self.prices.items():
            if crop in user_msg:
                extra = f"【本地行情参考（2025年5月）】{crop}：{json.dumps(info, ensure_ascii=False)}\n"
                break
        if extra:
            user_msg = extra + "\n农户问题：" + user_msg
        return super().chat(user_msg, history)
