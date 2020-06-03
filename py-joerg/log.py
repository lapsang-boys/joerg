import logging


def new_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.propagate = False
    logger.setLevel(level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
