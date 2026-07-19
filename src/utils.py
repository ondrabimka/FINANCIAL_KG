import logging
import logging.handlers
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"


def setup_custom_logger(name):
    # logger settings
    log_file = "logs.log"
    log_file_max_size = 1024 * 1024 * 20  # megabytes
    log_num_backups = 3
    log_format = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"

    # setup logger
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    log_formatter = logging.Formatter(log_format)

    rotate_file = logging.handlers.RotatingFileHandler(log_file, maxBytes=log_file_max_size, backupCount=log_num_backups)
    rotate_file.setFormatter(log_formatter)
    logger.addHandler(rotate_file)

    # print log messages to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger
