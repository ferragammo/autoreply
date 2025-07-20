import os
import pathlib
from functools import lru_cache
from langchain_openai import ChatOpenAI
import motor.motor_asyncio
from pymongo import MongoClient
from openai import AsyncClient

from dotenv import load_dotenv


load_dotenv()

class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent
    HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
    # LLM_MINI = ChatOpenAI(model="gpt-4.1-mini", temperature=0.3, use_responses_api=True)
    # DB_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_DB_URL")).reply
    # MONGO_CLIENT = MongoClient(os.getenv('MONGO_DB_URL'))
    # OPENAI_CLIENT = AsyncClient(api_key=os.getenv('OPENAI_API_KEY'))


class DevelopmentConfig(BaseConfig):
    Issuer = "http://localhost:8000"
    Audience = "http://localhost:3000"


class ProductionConfig(BaseConfig):
    Issuer = ""
    Audience = ""


@lru_cache()
def get_settings() -> DevelopmentConfig | ProductionConfig:
    config_cls_dict = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
    }
    config_name = os.getenv('FASTAPI_CONFIG', default='development')
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()


