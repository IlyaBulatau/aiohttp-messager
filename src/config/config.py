from typing import Any
from environs import Env

class BaseConfig:
    """
    Base config class
    """
    env = Env()
    env.read_env()

    APP_PORT = env('APP_PORT')
    APP_HOST = env('APP_HOST')

    EMAIL_ADDRESS = env('EMAIL_ADDRESS')
    EMAIL_PASSWORD = env('EMAIL_PASSWORD')

    POSTGRES_LOGIN = env('POSTGRES_LOGIN')
    POSTGRES_PASSWORD = env('POSTGRES_PASSWORD')
    POSTGRES_HOST = env('POSTGRES_HOST')
    POSTGRES_NAME = env('POSTGRES_NAME')

    def __getitem__(self, key: str) -> str:
        return getattr(self, key)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        raise AttributeError
    
    def __setitem__(self, key: Any, val: str) -> None:
        raise AttributeError


class DevelopmentConfig(BaseConfig):
    ...


class ProductConfig(BaseConfig):
    ...

