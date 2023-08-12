import asyncpg
from aiohttp import web


async def create_tablse(app: web.Application) -> None:
    """
    This func create all tablse in the database
    """
    connect: asyncpg.Connection = app['db']

    query_create_users_table = \
        """
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            username CHARACTER(20) NOT NULL UNIQUE
        );
        """
    query_create_messages_table = \
        """
        CREATE TABLE IF NOT EXISTS messages(
            message_id SERIAL PRIMARY KEY,
            body TEXT NOT NULL,
            user_id INT REFERENCES users (user_id),
            chat_id INT REFERENCES chats (chat_id)
        );
        """
    query_create_chats_table = \
        """
        CREATE TABLE IF NOT EXISTS chats(
            chat_id SERIAL PRIMARY KEY,
            name CHARACTER(20) NOT NULl
        );
        """
    
    query_create_users_chats_table = \
        """
        CREATE TABLE IF NOT EXISTS users_chats(
            user_id SERIAL REFERENCES users (user_id),
            chat_id SERIAL REFERENCES chats (chat_id),
            CONSTRAINT chat_user_id PRIMARY KEY (user_id, chat_id)
        );
        """
    query_list = [
        query_create_users_table,
        query_create_chats_table,
        query_create_messages_table,
        query_create_users_chats_table,
    ]

    for query in query_list:
        await connect.execute(query=query)