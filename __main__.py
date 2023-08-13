from src.app.routes import setup_router
from src.config.setup import setup_config
from src.logger.setup import setup_loggger
from src.database.connect import connect_with_database, close_connect_with_database
from src.database.models import create_tablse
from src.utils.user_sessions import setup_redis, AuthPolicy
from src.utils.context_processors import context_user_is_anonymous_processor, context_get_username_processor
from src.utils.decorators import add_user_id_to_request_middleware

from aiohttp import web
import aiohttp_jinja2
import jinja2
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy

import pathlib

app = web.Application()

def setup_templates(app: web.Application) -> None:  
    path_to_templates = pathlib.Path().absolute().joinpath('src').joinpath('app').joinpath('templates') 
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(searchpath=path_to_templates), 
                         context_processors=[context_user_is_anonymous_processor,
                                            context_get_username_processor, 
                                            aiohttp_jinja2.request_processor,
                                            ])

def setup_app(app: web.Application) -> None:
    path_to_static = pathlib.Path().absolute().joinpath('src').joinpath('static') 

    setup_config(app)
    setup_router(app, path_to_static=path_to_static)
    setup_redis(app)
    setup_session(app=app, storage=RedisStorage(app['redis']))
    setup_security(app, identity_policy=SessionIdentityPolicy(), autz_policy=AuthPolicy())
    setup_loggger(app, app['config']['EMAIL_ADDRESS'], app['config']['EMAIL_PASSWORD'])
    setup_templates(app)

    app['websockets'] = []

    app.middlewares.append(add_user_id_to_request_middleware)

    app.on_startup.append(connect_with_database)
    app.on_startup.append(create_tablse)
    app.on_shutdown.append(close_connect_with_database)

if __name__ == "__main__":
    setup_app(app)
    app['log'].warning('START MESSEGER APP')
    web.run_app(app, port=app['config']['APP_PORT'], host=app['config']['APP_HOST'])

# TODO - create chat-romms and setup websockets
