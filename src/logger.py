import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Sets up and returns a structured JSON logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if already added.
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
