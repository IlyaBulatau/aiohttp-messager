import aioredis
from aiohttp import web
from aiohttp_security import AbstractAuthorizationPolicy


def setup_redis(app: web.Application) -> aioredis.Redis:
    """
    Add redis storage in the app
    """
    redis = aioredis.Redis(host=app['config']['REDIS_HOST'])

    app['redis'] = redis


    
class AuthPolicy(AbstractAuthorizationPolicy):
    """
    Responsible for user auth
    """
    def permits(self, identity: int, permission: str, context=None) -> bool:
        return super().permits(identity, permission, context)
    
    def authorized_userid(self, identity: int) -> int:
        return super().authorized_userid(identity)

