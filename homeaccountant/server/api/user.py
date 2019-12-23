import re
import base64
import logging
import psycopg2.errors

from uuid import uuid4
from hashlib import sha256
from aiohttp import web
from psycopg2.errors import UniqueViolation

from homeaccountant import config
from homeaccountant.log.logger import getLogger
from homeaccountant.db.utils import User

logger = getLogger()

user_routes = web.RouteTableDef()

regex_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
try:
    regex_email_allowed = re.compile(config.SERVER.REGISTRATION.REGEX)
except:
    regex_email_allowed = re.compile(r'.*')
basic_regex = re.compile(r'Basic\s(?P<auth>.*)$')
bearer_regex = re.compile(r'Bearer\s(?P<token>.*)$')


@user_routes.get('/user')
async def getUser(request):
    try:
        userlogin = await request.app.storage.get_user(User(uid=request['user_id']))
        return web.json_response(data={
            'email': userlogin.email,
            'display_name': userlogin.display_name
        })
    except Exception as e:
        logger.exception(e)


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
            logger.debug('Failed to match regex : {}'.format(email))
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
        logger.debug('Trying to register {}'.format(userlogin))
        if (await request.app.storage.get_user(userlogin)):
            logger.debug('{} is already used'.format(userlogin.email))
            raise web.HTTPOk
        if config.SERVER.REGISTRATION.EMAIL_CONFIRMATION:
            token = base64.b64encode(
                sha256(str(userlogin).encode('utf8')).digest()).decode('utf8')
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
        raise


@user_routes.get('/user/login')
async def loginUser(request):
    try:
        try:
            authorization = request.headers['Authorization']
        except KeyError:
            raise web.HTTPUnauthorized
        basic = basic_regex.match(authorization)
        bearer = bearer_regex.match(authorization)
        if basic:
            try:
                auth = base64.b64decode(basic.group(
                    'auth').encode('utf8')).decode('utf8')
                email, password = auth.split(':', 1)
            except:
                raise web.HTTPUnauthorized
            userlogin = User(email, None, None)
            userlogin = await request.app.storage.get_user(userlogin)
            if userlogin == None:
                raise web.HTTPBadRequest
            password_hash = sha256('{}{}'.format(
                password, userlogin.password_salt).encode('utf8')).hexdigest()
            if password_hash == userlogin.password_hash:
                tokens = request.app.tokenmanager.generate_session_tokens(
                    userlogin.uid)
                return web.json_response(data={
                    'auth_token': tokens['auth'],
                    'refresh_token': tokens['refresh']
                })
            else:
                raise web.HTTPUnauthorized
        elif bearer:
            token = bearer.group('token')
            auth_token = request.app.tokenmanager.refresh_auth_token(token)
            if auth_token:
                return web.json_response(data={
                    'auth_token': auth_token,
                    'refresh_token': token
                })
            else:
                raise web.HTTPUnauthorized
        else:
            raise web.HTTPUnauthorized
    except web.HTTPError:
        raise
    except Exception as e:
        logger.exception(e)
        raise


@user_routes.get('/user/logout')
async def logoutUser(request):
    try:
        request.app.tokenmanager.revoke_tokens(request['auth_token'])
    except web.HTTPError:
        raise
    except Exception as e:
        logger.exception(e)
        raise
