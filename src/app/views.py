from aiohttp import web
import aiohttp_jinja2
from aiohttp_security import authorized_userid


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    ui = await authorized_userid(request)
    print(ui)
    return {'title': 'Home'}

@aiohttp_jinja2.template('index.html')
async def socket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await ws.send_str('Hello from server')  
    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            text = msg.data
            print(text)

        await ws.send_str(data=text+"/answer")
    return ws

