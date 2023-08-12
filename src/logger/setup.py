import logging

from src.logger.handlers import HANDLERS

def setup_loggger(app, email: str, passwod: str) -> None:
    """
    Create logger object and add all handlers from HANDLERS list

    email: app['config']['EMAIL_ADDRESS']
    password: app['config']['EMAIL_PASSWORD']
    """
    logger = logging.getLogger(__name__)

    for handler in HANDLERS:
        logger.addHandler(handler)


    app['log'] = logger