import openai
from typing import List, Dict

class BaseAgent:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.name = "BaseAgent"
        self.system_prompt = "你是一个有用的农业助手，用通俗易懂的中文回答农户问题。"

    def chat(self, user_msg: str, history: List[Dict] = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            for h in history[-6:]:  # 保留最近3轮
                messages.append({"role": "user", "content": h.get("user", "")})
                messages.append({"role": "assistant", "content": h.get("reply", "")})
        messages.append({"role": "user", "content": user_msg})
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1200
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"【服务暂时异常】{str(e)}，请检查API Key或网络。"

    def route(self, user_msg: str) -> bool:
        return False
