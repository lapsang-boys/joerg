import logging


def new_logger(name: str) -> logging.Logger:
    logger = logging.getLogger("asdf")
    logger.handlers = []
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
