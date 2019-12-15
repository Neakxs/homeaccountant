import re
import base64
import logging
import psycopg2.errors

from uuid import uuid4
from hashlib import sha256
from aiohttp import web
from psycopg2.errors import UniqueViolation

from homeaccountant import config
from homeaccountant.db.utils import User

user_routes = web.RouteTableDef()

regex_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
try:
    regex_email_allowed = re.compile(config.SERVER.REGISTRATION.REGEX)
except:
    regex_email_allowed = re.compile(r'.*')


@user_routes.get('/user')
async def getUser(request):
    raise NotImplementedError


@user_routes.put('/user')
async def putUser(request):
    raise NotImplementedError


@user_routes.post('/user/register')
async def registerUser(request):
    if not config.SERVER.REGISTRATION.ALLOW:
        raise web.HTTPForbidden
    try:
        data = await request.json()
        email = data['email']
        if not (regex_email.match(email) and regex_email_allowed.match(email)):
            raise web.HTTPBadRequest
        password_salt = uuid4().hex
        password_hash = sha256('{}{}'.format(
            data['password'], password_salt).encode('utf8')).hexdigest()
        if config.SERVER.REGISTRATION.ADMIN_CONFIRMATION:
            enabled = False
        else:
            enabled = True
        userlogin = User(email=email, password_hash=password_hash,
                         password_salt=password_salt, enabled=enabled)
        if (await request.app.storage.get_user(userlogin)):
            raise web.HTTPOk
        if config.SERVER.REGISTRATION.EMAIL_CONFIRMATION:
            token = base64.b64encode(str(userlogin)).decode('utf8')
            await request.app.cache.write_variable(token, userlogin.__dict__, expire=900)
            await request.app.sendmail.send_token(email, 'HomeAccountant Registration', token)
        else:
            try:
                userlogin = await request.app.storage.add_user(userlogin)
            except UniqueViolation:
                pass
        raise web.HTTPOk
    except web.HTTPError:
        raise
    except Exception:
        raise


@user_routes.get('/user/confirm')
async def confirmUser(request):
    try:
        token = request.rel_url.query['token']
        userlogin = User(**(await request.app.cache.read_variable(token)))
        try:
            userlogin = await request.app.storage.add_user(userlogin)
        except UniqueViolation:
            pass
        raise web.HTTPOk
    except Exception:
        raise web.HTTPNotFound


@user_routes.get('/user/login')
async def loginUser(request):
    raise NotImplementedError


@user_routes.get('/user/logout')
async def logoutUser(request):
    raise NotImplementedError
