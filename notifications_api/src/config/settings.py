from pathlib import Path

from pydantic_settings import BaseSettings


path = Path(__file__).parent


class Settings(BaseSettings):

    class Config:
        env_file = str(path / ".env")

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_QUEUE: str
    LOGGER_NAME: str
    LOG_LEVEL: str = "INFO"
    TEMPLATE_SERVICE: str
    TEMPLATE_SERVICE_PORT: int
    APP_AUTH_TOKEN: str

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    @property
    def template_service_url(self) -> str:
        return f"http://{self.TEMPLATE_SERVICE}:{self.TEMPLATE_SERVICE_PORT}/api/v1/admin/templates/static"


settings = Settings()
