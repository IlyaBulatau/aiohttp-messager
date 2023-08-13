import logging
from logging.handlers import SMTPHandler
from pathlib import Path

formatter = logging.Formatter(fmt="{asctime} | {levelname} | {message}", style="{")

# path to log.log fie
LOG_FILE_NAME = "log.log"
path_to_log_file = (
    Path().absolute().joinpath("src").joinpath("logger").joinpath(LOG_FILE_NAME)
)

stream_handler = logging.StreamHandler()
stream_handler.setLevel("DEBUG")
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(
    filename=path_to_log_file, mode="a", encoding="utf-8"
)
file_handler.setLevel("DEBUG")
file_handler.setFormatter(formatter)


def create_smtp_handler(email: str, password: str) -> SMTPHandler:
    """
    Create SMTP Handler to send logs by email

    email: app['config']['EMAIL_ADDRESS']
    password: app['config']['EMAIL_PASSWORD']
    """

    smtp_handler = SMTPHandler(
        mailhost=("smtp.yandex.ru", 587),
        fromaddr=email,
        toaddrs=email,
        subject="From Messager APP",
        credentials=(email, password),
        secure=(),
    )
    smtp_handler.setLevel("WARNING")
    smtp_handler.setFormatter(formatter)

    return smtp_handler


HANDLERS = [stream_handler, file_handler]
