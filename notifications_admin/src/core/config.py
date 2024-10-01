from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


ENV_PATH = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    """Класс настроек приложения."""

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding='utf-8',
        extra='ignore',
    )

    app_name: str = "Notification Admin"
    app_description: str = "Api for notification admin"
    app_version: str = "0.1.0"

    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_database: str = "database"
    db_schema: str = "notifications"

    notification_service_host: str = "notification-service"
    notification_service_port: int = 8080
    notification_endpoint: str = "/api/v1/send-notification"
    notification_auth_token: str = ''

    logger_filename: str = ...
    logger_filedir: str = ...
    logger_maxbytes: int = 15000000
    logger_mod: str = 'a'
    logger_backup_count: int = 5
    logger_name: str = 'not-admin'
    log_level: str = "INFO"

    @property
    def notiification_service_url(self) -> str:
        return (f"http://{self.notification_service_host}:"
                f"{self.notification_service_port}"
                f"{self.notification_endpoint}")

    @property
    def logger_file(self) -> str:
        return f"{self.logger_filedir}/{self.logger_filename}"


settings = Settings()
