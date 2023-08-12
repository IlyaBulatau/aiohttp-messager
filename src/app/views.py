from aiohttp import web
import aiohttp_jinja2
from aiohttp_security import authorized_userid

from src.utils.decorators import login_verification

@login_verification
@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> web.Response:
    user_id = await authorized_userid(request)
    print(user_id)
    return {'title': 'Home'}

@aiohttp_jinja2.template('index.html')
async def socket_handler(request) -> web.Response:
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await ws.send_str('Hello from server')  
    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            text = msg.data
            print(text)

        await ws.send_str(data=text+"/answer")
    return ws

