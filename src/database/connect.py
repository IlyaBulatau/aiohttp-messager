import asyncpg
from aiohttp import web


async def connect_with_database(app: web.Application) -> None:
    """
    Create database if it is doesnt exist
    And add connect to app
    """
    connect: asyncpg.Connection = await asyncpg.connect(
        host=app["config"]["POSTGRES_HOST"],
        user=app["config"]["POSTGRES_LOGIN"],
        password=app["config"]["POSTGRES_PASSWORD"],
    )
    database_name: str = app["config"]["POSTGRES_NAME"]

    if not await check_if_database_is_exist(connect, database_name):
        await create_database(connect, database_name)

    new_connect: asyncpg.Connection = await asyncpg.connect(
        host=app["config"]["POSTGRES_HOST"],
        user=app["config"]["POSTGRES_LOGIN"],
        password=app["config"]["POSTGRES_PASSWORD"],
        database=database_name,
    )
    app["db"] = new_connect


async def create_database(connect: asyncpg.Connection, database_name: str) -> None:
    """
    Create database func
    And close connect
    """
    query = f"CREATE DATABASE {database_name}"
    await connect.execute(query=query)

    await connect.close()


async def check_if_database_is_exist(
    connect: asyncpg.Connection, database_name: str
) -> bool:
    """
    Check exist database
    """
    query = (
        f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{database_name}'"
    )
    database_is_exist = await connect.execute(query=query)
    if database_is_exist == "SELECT 0":
        return False
    return True


async def close_connect_with_database(app: web.Application) -> None:
    """
    Close connect with database
    """
    await app["db"].close()
