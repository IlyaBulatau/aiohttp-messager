from src.app.view import index, socket_handler

from aiohttp import web


def setup_router(app: web.Application, path_to_static) -> None:
    app.router.add_get('/', index, name='index')
    app.router.add_get('/sock', socket_handler)
    app.router.add_get('/{name}', index)

    app.router.add_static(prefix='/static', path=path_to_static, name='static')

    