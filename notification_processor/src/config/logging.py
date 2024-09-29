import logging
from config.settings import settings


def get_logger(name: str):
    logger = logging.getLogger(name)

    logger.setLevel(settings.log_level)

    handler = logging.StreamHandler()
    handler.setLevel(settings.log_level)

    formatter = logging.Formatter(
        '{"time": "%(asctime)-s", "level": "%(levelname)-s", "message": "%(message)s", "filename": "%(filename)s", "line": %(lineno)d}',
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
