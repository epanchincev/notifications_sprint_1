import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOG_CONFIG

load_dotenv()

# Применяем настройки логирования
logging_config.dictConfig(LOG_CONFIG)


class Settings(BaseSettings):
    project_name: str = "Kafka Fetcher"
    debug: bool = False
    port: int = 5000
    brokers: list

    model_config = SettingsConfigDict(env_prefix="FETCHER_")


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
