from src.config.config import DevelopmentConfig, ProductConfig

import argparse

from aiohttp.web import Application

def setup_config(app: Application) -> None:
    """
    Setup config for app

    If parse argument have arg --product then set Produc config else Dev config
    """
    arguments = parse_arguments()
    product: int = arguments.product
    if product:
        app['config'] = ProductConfig()
    else:
        app['config'] = DevelopmentConfig()

def parse_arguments() -> argparse.Namespace:
    """
    This func parge argument from command line
    """
    parser = argparse.ArgumentParser(description='Arguments for run app')
    parser.add_argument('-p', '--product', type=int, default=0)

    return parser.parse_args()
