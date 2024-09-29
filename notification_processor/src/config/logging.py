import logging
from config.settings import settings


def setup_logging():
    logging.basicConfig(
        level=settings.log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


def get_logger(name: str):
    return logging.getLogger(name)
