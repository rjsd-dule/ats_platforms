import logging
import json
import os
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.__dict__.get("extra"):
            log_record.update(record.__dict__["extra"])
        return json.dumps(log_record)

def get_logger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    console_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s "
        "| %(message)s "
        "[%(module)s:%(lineno)d]",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        }
    )

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s | %(module)s:%(lineno)d"
    )

    json_formatter = JsonFormatter()

    handlers = [
        ("app-debug.log", logging.DEBUG, file_formatter),
        ("app-info.log", logging.INFO, file_formatter),
        ("app-error.log", logging.ERROR, file_formatter),
        ("app.json.log", logging.INFO, json_formatter),
    ]

    for filename, level, formatter in handlers:
        handler = TimedRotatingFileHandler(
            os.path.join(LOG_DIR, filename),
            when="midnight",
            backupCount=30,
            encoding="utf-8"
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

logger = get_logger()