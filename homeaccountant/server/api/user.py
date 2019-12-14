import re
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
        password_hash = sha256('{}{}'.format(data['password'], password_salt).encode('utf8')).hexdigest()
        userlogin = User(email=email, password_hash=password_hash, password_salt=password_salt, enabled=False)
        # try:
        #     userlogin = await request.app.storage.add_user(userlogin) # Send JWT with info to store in mail
        # except UniqueViolation:
        #     raise web.HTTPOk
        # Send mail for user confirmation
    except web.HTTPError:
        raise
    except Exception as e:
        raise

@user_routes.get('/user/confirm')
async def confirmUser(request):
    raise NotImplementedError

@user_routes.get('/user/login')
async def loginUser(request):
    raise NotImplementedError

@user_routes.get('/user/logout')
async def logoutUser(request):
    raise NotImplementedError