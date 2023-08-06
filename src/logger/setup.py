import logging
from logging.handlers import SMTPHandler
from src.logger.handlers import create_smtp_handler, HANDLERS

def setup_loggger(email: str, passwod: str) -> logging.Logger:
    """
    Create logger object and add all handlers from HANDLERS list

    email: app['config']['EMAIL_ADDRESS']
    password: app['config']['EMAIL_PASSWORD']
    """
    logger = logging.getLogger(__name__)

    for handler in HANDLERS:
        logger.addHandler(handler)


    return logger