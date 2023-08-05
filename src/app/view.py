from aiohttp import web
import aiohttp_jinja2


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    return {'title': 'title'}

async def socket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await ws.send_str('Hello from server')  
    async for msg in ws:
        print(msg)
        await ws.send_str(data=msg.data+"/answer")
    return ws