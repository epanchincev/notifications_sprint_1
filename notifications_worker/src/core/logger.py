# LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FORMAT = (
    '{"time": "%(asctime)-s", "level": "%(levelname)-s", "message": "%(message)s"}'
)
LOG_LEVEL = "DEBUG"

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "json": {
            "format": LOG_FORMAT,
        },
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
            "filename": "/var/log/fetcher/fetcher-app.log",
            "formatter": "json",
        },
    },
    "root": {"level": LOG_LEVEL, "handlers": ["console", "file"]},
}
