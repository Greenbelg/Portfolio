import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import src.config as config
from logging.handlers import RotatingFileHandler


def configure_logger(logfile, loglevel):
    logger = logging.getLogger(config.LOGGER_FILE)
    logger.setLevel(loglevel)

    file_handler = RotatingFileHandler(
        logfile, 
        maxBytes = config.MAX_LOG_IN_BYTES,
        backupCount = config.LOG_BACKUP_COUNT)
    file_handler.setLevel(loglevel)

    formatter = logging.Formatter(config.LOGGER_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
