import logging
import json
import uuid
import os
from logging.handlers import RotatingFileHandler


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "trace_id"):
            log_record["trace_id"] = record.trace_id

        return json.dumps(log_record)


def setup_logger(
    name="minidb",
    log_file="logs/minidb.log",
    level=logging.INFO
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Formatters
    json_formatter = JSONFormatter()
    text_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(json_formatter)
    console_handler.setFormatter(text_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def new_trace_id():
    return str(uuid.uuid4())
