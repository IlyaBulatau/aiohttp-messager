"""
Processors for jinjia2
"""
from aiohttp_security import is_anonymous, authorized_userid
from aiohttp import web
from asyncpg import Connection

from src.utils.queries import get_user_in_db_by_id

async def context_user_is_anonymous_processor(request: web.Request) -> dict:
    result_bool: bool =  await is_anonymous(request)
    return {'is_anonymous': result_bool}

async def context_get_username_processor(request: web.Request) -> dict:
    user_id: str = await authorized_userid(request)

    db: Connection = request.app['db']

    result = await db.fetchrow(get_user_in_db_by_id, int(user_id))

    username = dict(result).get('username')

    return {'username': username}