import psycopg2.errors

from aiohttp import web
from psycopg2.errors import UniqueViolation

from homeaccountant import config
from homeaccountant.log.logger import getLogger
from homeaccountant.db.utils import Account, User

logger = getLogger()

account_routes = web.RouteTableDef()


###################
# READ OPERATIONS #
###################

@account_routes.get('/account')
async def getAccount(request):
    try:
        data = await request.json()
        account_uid, name, acronym = None, None, None
        if 'account_uid' in data:
            account_uid = data['account_uid']
        elif 'name' in data:
            name = data['name']
        else:
            acronym = data['acronym']
        user_uid = request['user_uid']
        try:
            if account_uid:
                account = await request.app.storage.get_account_from_uid(account_uid, user_uid)
            elif name:
                account = await request.app.storage.get_account_from_name(name, user_uid)
            else:
                account = await request.app.storage.get_account_from_acronym(acronym, user_uid)
            if account:
                return web.json_response(data={
                    'uid': account.uid,
                    'name': account.name,
                    'balance': account.balance,
                    'acronym': account.acronym,
                    'user': str(account.user)
                })
        except ValueError:
            raise
        raise web.HTTPOk
    except Exception:
        raise
    

@account_routes.get('/accounts')
async def getAccounts(request):
    raise NotImplementedError


#####################
# CREATE OPERATIONS #
#####################

@account_routes.post('/account')
async def registerAccount(request):
    try:
        data = await request.json()
        name = data['name']
        balance = data['balance']
        acronym = data['acronym']
        user_uid = request['user_uid']
        try:
            user = await request.app.storage.get_user(User(uid=user_uid))
        except ValueError:
            raise
        account = Account(
            name=name,
            balance=balance,
            acronym=acronym,
            user=user
        )
        logger.debug('Trying to add {}'.format(account))
        if (await request.app.storage.get_account_from_name(name, user_uid) or await request.app.storage.get_account_from_acronym(acronym, user_uid)):
            logger.debug('{} is already used'.format(str(account)))
            raise web.HTTPOk
        else:
            try:
                account = await request.app.storage.add_account(account)
            except UniqueViolation:
                pass
        raise web.HTTPOk
    except web.HTTPError:
        raise
    except Exception:
        raise



#####################
# UPDATE OPERATIONS #
#####################

@account_routes.put('/account')
async def putAccount(request):
    raise NotImplementedError



#####################
# DELETE OPERATIONS #
#####################

@account_routes.delete('/account')
async def deleteAccount(request):
    raise NotImplementedError