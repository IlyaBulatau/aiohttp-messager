import functools
from typing import Callable, Coroutine

from aiohttp import web
from aiohttp_security import authorized_userid, is_anonymous


def login_verification(coro: Coroutine) -> Callable:
    """
    Verificat user session
    """

    @functools.wraps(coro)
    async def wrapper(*args, **kwargs) -> web.Response:
        request: web.Request = args[0]

        if await is_anonymous(request):
            return web.HTTPFound("/login")

        return await coro(*args, **kwargs)

    return wrapper


@web.middleware
async def add_user_id_to_request_middleware(
    request: web.Request, handler: Callable
) -> web.Response:
    """
    Add user_id to request objects
    """
    user_id = await authorized_userid(request)

    request.user_id = user_id

    return await handler(request)
