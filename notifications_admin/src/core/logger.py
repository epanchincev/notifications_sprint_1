import logging
import uuid
from contextvars import ContextVar

from core.config import settings
import os

ctx_request_id: ContextVar[str] = ContextVar('request_id')

LOG_FORMAT = ('{"request_id": "%(request_id)s", "asctime": '
              '"%(asctime)s", "levelname": "%(levelname)s", '
              '"name": "%(name)s", "message": "%(message)s", '
              '"host": "%(host)s", "user-agent": "%(user-agent)s", '
              '"method": "%(method)s", "path": "%(path)s", '
              '"query_params": "%(query_params)s", '
              '"status_code": "%(status_code)s"}')


def setup_root_logger():
    logger = logging.getLogger('')
    if logger.hasHandlers():
        logger.handlers.clear()
    formatter = logging.Formatter(LOG_FORMAT)
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    if not os.path.exists(settings.logger_file):
        os.makedirs(settings.logger_filedir, exist_ok=True)
        open(settings.logger_file, 'w').close()

    file = logging.handlers.RotatingFileHandler(
        filename=settings.logger_file,
        mode=settings.logger_mod,
        maxBytes=settings.logger_maxbytes,
        backupCount=settings.logger_backup_count,
    )
    file.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file)
    logger.setLevel(logging.INFO)

    factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = factory(*args, **kwargs)
        record.request_id = ctx_request_id.get(uuid.uuid4())
        return record

    logging.setLogRecordFactory(record_factory)
