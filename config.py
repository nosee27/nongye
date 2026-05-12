import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "yunzhichain-dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///yunzhichain.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 硬编码，优先级最高
    OPENAI_API_KEY = "sk-f37bf04299be4e1d9c2951fddc74f589"
    OPENAI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    MODEL_NAME = "qwen-plus"