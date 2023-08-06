from src.app.routes import setup_router
from src.config.setup import setup_config
from src.logger.setup import setup_loggger

from aiohttp import web
import aiohttp_jinja2
import jinja2
import pathlib

app = web.Application()

def setup_templates(app: web.Application) -> None:
    path_to_templates = pathlib.Path().absolute().joinpath('src').joinpath('app').joinpath('templates') 
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(searchpath=path_to_templates))

def setup_app(app: web.Application) -> None:
    path_to_static = pathlib.Path().absolute().joinpath('src').joinpath('static') 

    setup_config(app)
    setup_templates(app)
    setup_router(app, path_to_static=path_to_static)


if __name__ == "__main__":
    setup_app(app)
    log = setup_loggger(app['config']['EMAIL_ADDRESS'], app['config']['EMAIL_PASSWORD'])
    log.warning('START MESSEGER APP')
    web.run_app(app, port=app['config']['APP_PORT'], host=app['config']['APP_HOST'])

