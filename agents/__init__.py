from .planting_agent import PlantingAgent
from .pest_agent import PestAgent
from .market_agent import MarketAgent
from .trade_agent import TradeAgent

AGENT_MAP = {
    "种植规划": PlantingAgent,
    "病虫害诊断": PestAgent,
    "市场行情": MarketAgent,
    "产销对接": TradeAgent,
}

def get_agent(agent_name: str, api_key: str, base_url: str, model: str):
    agent_cls = AGENT_MAP.get(agent_name)
    if agent_cls:
        return agent_cls(api_key, base_url, model)
    return None
