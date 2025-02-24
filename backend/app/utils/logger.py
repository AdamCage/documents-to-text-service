import logging


def get_logger(name: str) -> logging.Logger:
    """_summary_

    Args:
        name (str): _description_

    Returns:
        logging.Logger: _description_
    """
    logger = logging.getLogger(name)

    return logger
