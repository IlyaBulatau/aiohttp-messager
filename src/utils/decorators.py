import functools
from typing import Coroutine, Callable

from aiohttp import web
from aiohttp_security import is_anonymous

def login_verification(coro: Coroutine) -> Callable:
    """
    Verificat user session
    """

    @functools.wraps(coro)
    async def wrapper(*args, **kwargs) -> web.Response:
        request: web.Request = args[0] 

        if await is_anonymous(request):
            return web.HTTPFound('/login')
        
        return await coro(*args, **kwargs)
    
    return wrapper