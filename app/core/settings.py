from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Config(BaseSettings):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MONGO_DB_CONNECTION_STRING: str = os.getnenv("MONGODB_CONNECTION_STRING")

_settings_instance: Config | None = None

def get_settings() -> Config:
    global _settings_instance

    if _settings_instance is None:
        _settings_instance = Config()

    return _settings_instance