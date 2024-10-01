import logging
import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv()


class RabbitMQSettings(BaseSettings):
    user: str = Field("rabbit", alias="DEFAULT_USER")
    password: str = Field("rabbit", alias="DEFAULT_PASS")
    host: str = Field("rabbit")
    port: int = 5672

    model_config = SettingsConfigDict(env_prefix="RABBITMQ_")

    def get_url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class Settings(BaseSettings):
    project_name: str = "Notification worker"
    queue: RabbitMQSettings = RabbitMQSettings()
    log_level: str = "INFO"

    sendsay_apikey: str
    sendsay_login: str

    logger_debug: bool = True
    logger_filename: str = "worker-app.log"
    logger_name: str = "notifier.logger"

    queue_name: str = "notification.sending"
    queue_exchange_name: str = "notifier"
    queue_consumer_tag: str = "worker1"
    queue_prefetch_count: int = 1


settings = Settings()


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
