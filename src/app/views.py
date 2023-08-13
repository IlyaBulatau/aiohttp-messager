import asyncio

import aiohttp_jinja2
from aiohttp import web
from asyncpg import Connection

from src.utils.decorators import login_verification
from src.utils.queries import (
    get_chat_by_id,
    get_chats_in_db,
    insert_chat_in_chats_table,
)


@login_verification
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> web.Response:
    """
    /
    Home Page
    """
    method = request.method.upper()

    if method == "GET":
        db: Connection = request.app["db"]

        # get all chat from db
        res = await db.fetch(query=get_chats_in_db)
        chats: list[tuple(str, str)] = [
            (dict(r).get("name"), str((dict(r).get("chat_id")))) for r in res
        ]

        # write logging
        user_id: str = request.user_id
        request.app["log"].warning(f"USER SESSION ID {user_id}")

        return {"title": "Home", "chats": chats}

    elif method == "POST":
        data_in_form = await request.post()
        chat_name = data_in_form.get("chat_name")

        db: Connection = request.app["db"]

        # create transaction, write chat in db
        async with db.transaction():
            await db.executemany(
                command=insert_chat_in_chats_table,
                args=[
                    (chat_name.strip(),),
                ],
            )

        return {"title": "Home"}


class WebSocket(web.View):
    @aiohttp_jinja2.template("chat.html")
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        user_id = self.request.user_id
        ws_list: list = self.request.app["websockets"]
        ws_list.append(ws)

        tasks_message_disconnect = []

        await self.broadcast_server_message(f"Join USER WITH ID {user_id}", ws_list)

        await self.broadcast_user_message(ws, ws_list)

        for _ws in ws_list:
            if _ws == ws:
                continue
            message = "User disconect"
            task = asyncio.create_task(_ws.send_str(message))
            tasks_message_disconnect.append(task)

        await asyncio.gather(*tasks_message_disconnect)

        if ws in ws_list:
            ws_list.remove(ws)

        return ws

    async def broadcast_server_message(
        self, message: str, ws_list: list[web.WebSocketResponse]
    ) -> None:
        tasks = []

        for _ws in ws_list:
            _ws: web.WebSocketResponse
            task = asyncio.create_task(_ws.send_str(message))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def broadcast_user_message(
        self, ws: web.WebSocketResponse, ws_list: list[web.WebSocketResponse]
    ) -> None:
        tasks = []

        async for msg in ws:
            if msg.type == web.WSMsgType.text:
                message = msg.data
                if message == "close":
                    ws_list.remove(ws)
                    await ws.close()
                else:
                    for _ws in ws_list:
                        task = asyncio.create_task(_ws.send_str(message))
                        tasks.append(task)

        await asyncio.gather(*tasks)


@aiohttp_jinja2.template("chat.html")
async def chat_room(request: web.Request):
    """
    /chat/{id}
    Page chat
    """
    method = request.method.upper()

    if method == "GET":
        id_ = request.match_info.get("id")

        db: Connection = request.app["db"]

        res = await db.fetchrow(get_chat_by_id, int(id_))
        chat_name = res.get("name")

        return {"title": "Chat Room", "chat_name": chat_name}
