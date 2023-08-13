from aiohttp import web
import aiohttp_jinja2
import asyncio

from src.utils.decorators import login_verification

@login_verification
@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> web.Response:
    method = request.method.upper()

    if method == 'GET':
        user_id = request.user_id
        request.app['log'].warning(f'USER SESSION ID {user_id}')
        return {'title': 'Home'}

    elif method == 'POST':
        data_in_form = await request.post()
        chat_name = data_in_form.get('chat_name')


class WebSocket(web.View):

    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        
        user_id = self.request.user_id
        ws_list: list = self.request.app['websockets']
        ws_list.append(ws)

        tasks_message_disconnect = []

        await self.broadcast_server_message(f'Join USER WITH ID {user_id}', ws_list)

        await self.broadcast_user_message(ws, ws_list)
        
        for _ws in ws_list:
            if _ws == ws:
                continue
            message = 'User disconect'
            task = asyncio.create_task(_ws.send_str(message))
            tasks_message_disconnect.append(task)

        await asyncio.gather(*tasks_message_disconnect)
    
        if ws in ws_list:
            ws_list.remove(ws)

        return ws

    async def broadcast_server_message(self, message: str, ws_list: list[web.WebSocketResponse]) -> None:
        tasks = []

        for _ws in ws_list:
            task = asyncio.create_task(_ws.send_str(message))
            tasks.append(task)

        await asyncio.gather(*tasks)
    
    async def broadcast_user_message(self, ws: web.WebSocketResponse, ws_list: list[web.WebSocketResponse]) -> None:
        tasks = []

        async for msg in ws:

            if msg.type == web.WSMsgType.text:
                message = msg.data
                if message == 'close':
                    ws_list.remove(ws)
                    await ws.close()
                else:
                    for _ws in ws_list:
                        task = asyncio.create_task(_ws.send_str(message))
                        tasks.append(task)

        await asyncio.gather(*tasks)


