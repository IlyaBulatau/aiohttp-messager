from aiohttp import web

from src.app.auth.views import auth, login, logout
from src.app.views import WebSocket, chat_room, index


def setup_router(app: web.Application, path_to_static) -> None:
    app.router.add_get("/", index, name="index")
    app.router.add_post("/", index)
    app.router.add_get("/sock", WebSocket, name="ws")
    app.router.add_get("/login", login, name="login")
    app.router.add_post("/login", login)
    app.router.add_get("/auth", auth, name="auth")
    app.router.add_post("/auth", auth)
    app.router.add_get("/logout", logout, name="logout")
    app.router.add_get("/chat/{id}", chat_room, name="chat_room")

    app.router.add_static(prefix="/static", path=path_to_static, name="static")
