import logging

from core.config import settings


logger = logging.getLogger(settings.logger_name)
logger.setLevel(settings.log_level)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '{"time": "%(asctime)-s", '
    '"level": "%(levelname)-s", "message": "%(message)s"}',
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_logger():
    return logger
