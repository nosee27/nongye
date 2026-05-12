from .base_agent import BaseAgent

class TradeAgent(BaseAgent):
    def __init__(self, api_key: str, base_url: str, model: str):
        super().__init__(api_key, base_url, model)
        self.name = "产销对接Agent"
        self.system_prompt = """你是【产销对接Agent】，帮助农户对接收购商、合作社、电商平台。
回答要求：
1. 列出可行的销售渠道及优缺点：
   - 本地收购商（快但价低）
   - 批发市场（量大但需运输）
   - 电商平台/直播（价高但需运营能力）
   - 社区团购（稳定但量小）
   - 合作社/龙头企业（有保障但需按标准种植）
2. 提醒合同签订要点：价格、质量标准、付款方式、违约责任
3. 货款安全：尽量货到付款或预付定金，警惕"打白条"
4. 如果农户有具体产品，给出1-2条最匹配的建议渠道"""

    def route(self, user_msg: str) -> bool:
        keywords = ["卖", "买", "收购", "渠道", "批发", "电商", "对接", "合作社", "老板",
                    "销路", "收购商", "贩子", "中间商", "直播", "拼多多", "淘宝", "社区团购",
                    "合同", "货款", "定金", "滞销"]
        return any(k in user_msg for k in keywords)
