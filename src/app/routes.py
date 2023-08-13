from src.app.views import index, WebSocket
from src.app.auth.views import login, auth, logout

from aiohttp import web


def setup_router(app: web.Application, path_to_static) -> None:
    app.router.add_get('/', index, name='index')
    app.router.add_view('/sock', WebSocket)
    app.router.add_get('/login', login, name='login')
    app.router.add_post('/login', login)
    app.router.add_get('/auth', auth, name='auth')
    app.router.add_post('/auth', auth)
    app.router.add_get('/logout', logout, name='logout')

    app.router.add_static(prefix='/static', path=path_to_static, name='static')

    