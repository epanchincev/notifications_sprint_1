from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    rabbitmq_host: str = "rabbit"
    rabbitmq_port: str = "5672"
    rabbitmq_user: str = "rabbit"
    rabbitmq_password: str = "rabbit"
    rabbitmq_in_queue: str = "notifications"
    rabbitmq_out_queue: str = "notification.sending"

    template_service_host: str = "notifications-admin"
    template_service_port: str = 8000
    auth_service_host: str = "fake-auth-service"
    auth_service_port: str = 8000

    log_level: str = "INFO"

    @property
    def rabbit_url(self):
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}"

    @property
    def template_service_url(self) -> str:
        return f"http://{self.template_service_host}:{self.template_service_port}"

    @property
    def auth_service_url(self) -> str:
        return f"http://{self.auth_service_host}:{self.auth_service_port}"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
