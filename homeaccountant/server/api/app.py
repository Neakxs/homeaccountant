
import re
import time
import asyncio

from aiohttp import web

from homeaccountant import config
from homeaccountant.server.api import user, transaction
from homeaccountant.server.types import Cookie
from homeaccountant.db import cache, storage

auth_regex = re.compile(r'.*/user/(login|register)$')


@web.middleware
async def authentication_middleware(request, handler):
    cache = request.app['cache']
    authorized = False
    try:
        auth_cookie = request.cookies[Cookie.AUTHENTICATION]
        expires = (await cache.read_variable(auth_cookie))['expiresAfter']
        if expires <= time.time_ns():
            authorized = True
    except KeyError:
        pass
    if not auth_regex.match(str(request.rel_url)) and not authorized:
        raise web.HTTPUnauthorized
    return await handler(request)


class WebAPI:
    def __init__(self):
        self.__app = web.Application(middlewares=[authentication_middleware])
        self.__app['cache'] = cache.Cache.create_cache()
        self.__app['storage'] = None
        self.__site = None
        self.__app.add_routes(user.user_routes)
        self.__app.add_routes(transaction.transaction_routes)

    def get_app(self):
        return self.__app

    async def run(self):
        runner = web.AppRunner(self.__app)
        await runner.setup()
        self.__site = web.TCPSite(
            runner, config.LISTEN_ADDRESS, config.LISTEN_PORT)
        await self.__site.start()


if __name__ == '__main__':
    api = WebAPI()
    asyncio.get_event_loop().run_until_complete(api.run())
    asyncio.get_event_loop().run_forever()
