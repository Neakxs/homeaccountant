import re
import time
import urllib
import asyncio
import smtplib

from aiohttp import web
from concurrent.futures import ThreadPoolExecutor

from homeaccountant import config
from homeaccountant.db.utils import User
from homeaccountant.log.logger import getLogger
from homeaccountant.server.api import user, transaction, bearer
from homeaccountant.db import cache, storage

logger = getLogger()

auth_regex = re.compile(r'.*/user/(login|register|confirm.*)$')
bearer_regex = re.compile(r'Bearer\s(?P<token>.*)$')

@web.middleware
async def authentication_middleware(request, handler):
    authorized = False
    try:
        try:
            token = bearer_regex.match(request.headers['Authorization']).group('token')
        except AttributeError:
            raise KeyError
        uid = request.app.tokenmanager.get_uid(token)
        if uid != None:
            request['auth_token'] = token
            request['user_uid'] = uid
            authorized = True
    except KeyError:
        pass
    if not auth_regex.match(str(request.rel_url)) and not authorized:
        raise web.HTTPUnauthorized
    return await handler(request)

class MailSender:
    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=2)
        if config.SERVER.SENDMAIL.USE_SSL:
            self._server = smtplib.SMTP_SSL(
                config.SERVER.SENDMAIL.HOSTNAME, config.SERVER.SENDMAIL.PORT)
        else:
            self._server = smtplib.SMTP(
                config.SERVER.SENDMAIL.HOSTNAME, config.SERVER.SENDMAIL.PORT)

    def _send_token(self, mail_to, subject, token):
        self._server.connect(config.SERVER.SENDMAIL.HOSTNAME,
                             config.SERVER.SENDMAIL.PORT)
        self._server.ehlo()
        self._server.login(config.SERVER.SENDMAIL.USERNAME,
                           config.SERVER.SENDMAIL.PASSWORD)
        msg = '''Subject: {subject}\r\n\r\nYou can confirm your registration by following this link : http://{domain}/user/confirm?token={token}'''.format(
            domain=config.SERVER.DOMAIN, subject=subject, token=urllib.parse.quote(token))
        self._server.sendmail(config.SERVER.SENDMAIL.USERNAME, mail_to, msg)
        self._server.quit()

    async def send_token(self, *args, **kwargs):
        if config.SERVER.SENDMAIL.ENABLED:
            asyncio.get_event_loop().run_in_executor(
                self._executor, self._send_token, *args, **kwargs)


class WebAPI:
    def __init__(self):
        self.__app = web.Application(middlewares=[authentication_middleware])
        self.__app.storage = None
        self.__app.tokenmanager = None
        self.__app.sendmail = MailSender()
        self.__site = None
        self.__app.add_routes(user.user_routes)
        self.__app.add_routes(transaction.transaction_routes)

    def get_app(self):
        return self.__app

    async def run(self):
        runner = web.AppRunner(self.__app)
        self.__app.storage = await storage.Storage.open_storage()
        self.__app.tokenmanager = bearer.TokenManager()
        await runner.setup()
        self.__site = web.TCPSite(
            runner, config.SERVER.HOSTNAME, config.SERVER.PORT)
        await self.__site.start()


if __name__ == '__main__':
    api = WebAPI()
    asyncio.get_event_loop().run_until_complete(api.run())
    asyncio.get_event_loop().run_forever()
