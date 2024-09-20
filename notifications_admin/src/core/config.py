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


settings = Settings()
