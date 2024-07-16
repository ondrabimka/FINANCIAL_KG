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
    # log_date_format = "%m/%d/%Y %I:%M:%S %p"
    log_filemode = "w"  # w: overwrite; a: append

    # setup logger
    # datefmt=log_date_format
    logging.basicConfig(filename=log_file, format=log_format, filemode=log_filemode, level=logging.DEBUG)
    rotate_file = logging.handlers.RotatingFileHandler(log_file, maxBytes=log_file_max_size, backupCount=log_num_backups)
    logger = logging.getLogger(name)
    logger.addHandler(rotate_file)

    # print log messages to console
    consoleHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(log_format)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger
