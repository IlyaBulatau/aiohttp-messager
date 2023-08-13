import redis.asyncio as aioredis
from aiohttp import web
from aiohttp_security import AbstractAuthorizationPolicy


def setup_redis(app: web.Application) -> aioredis.Redis:
    """
    Add redis storage in the app
    """
    url = f'redis://{app["config"]["REDIS_HOST"]}'
    redis = aioredis.from_url(url=url, decode_responses=True)

    app["redis"] = redis


class AuthPolicy(AbstractAuthorizationPolicy):
    """
    Responsible for user auth
    """

    async def permits(self, identity: int, permission: str, context=None) -> bool:
        return True

    async def authorized_userid(self, identity: int) -> int:
        return identity
