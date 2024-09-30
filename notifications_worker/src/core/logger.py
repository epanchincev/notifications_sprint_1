import logging
from logging import config as logging_config

from core.config import settings

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "json": {
            "format": '{"time": "%(asctime)-s", "level": "%(levelname)-s", "message": "%(message)s"}',
        },
        "default": {
            "format": "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": settings.logger_filename,
            "formatter": "json",
        },
    },
    "root": {"level": settings.log_level, "handlers": ["console", "file"]},
}

logging_config.dictConfig(LOG_CONFIG)

logger = logging.getLogger(settings.logger_name)
