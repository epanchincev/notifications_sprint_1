import logging

from .settings import settings


logger = logging.getLogger(settings.LOGGER_NAME)

logger.setLevel(settings.LOG_LEVEL)

handler = logging.StreamHandler()
handler.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter(
    '{"time": "%(asctime)-s", "level": "%(levelname)-s", "message": "%(message)s"}',
)
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Logger initialized")


def get_logger():
    return logger
