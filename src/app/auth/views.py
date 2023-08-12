from aiohttp import web
import aiohttp_jinja2
from asyncpg import Connection
from aiohttp_security import remember

from src.utils import queries

@aiohttp_jinja2.template('login.html')
async def login(request: web.Request):
    method = request.method.upper()

    if method == 'GET':
        return {'title': 'login'}
    
    elif method == 'POST':
        data_in_form: dict = await request.post()
        username: str = data_in_form.get('username')

        db: Connection = request.app['db']

        result = await db.fetchrow(queries.get_user_in_db_by_name, username)
        user_id = dict(result).get('user_id')

        await remember(request, web.HTTPFound('/'), str(user_id))

        return web.HTTPFound('/')
        
@aiohttp_jinja2.template('auth.html')
async def auth(request: web.Request):
    method = request.method.upper()

    if method == 'GET':
        return {'title': 'auth'}
    
    elif method == 'POST':
        data_in_form: dict = await request.post()
        username: str = data_in_form.get('username')
        
        db: Connection = request.app['db']

        r = await db.executemany(command=queries.insert_user_in_users_table, args=[(username,),])
        print(r)

        return web.HTTPFound('/login')