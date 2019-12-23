from aiohttp import web

from homeaccountant import config
from homeaccountant.log.logger import getLogger
from homeaccountant.db.utils import User, TransactionFamily, TransactionCategory

logger = getLogger()

transaction_routes = web.RouteTableDef()


###################
# READ OPERATIONS #
###################

@transaction_routes.get('/transactionfamily')
async def getTransactionFamily(request):
    try:
        data = await request.json()
        transaction_family_uid = data['transaction_family_uid']
        try:
            transaction_family = await request.app.storage.get_transaction_family_from_uid(transaction_family_uid)
            if transaction_family:
                return web.json_response(data={
                    'uid': transaction_family.uid,
                    'name': transaction_family.name
                })
        except ValueError:
            raise
        raise web.HTTPOk
    except Exception:
        raise


@transaction_routes.get('/transactioncategory')
async def getTransactionCategory(request):
    try:
        data = await request.json()
        transaction_category_uid, family_name, name = None, None, None
        if 'transaction_category_uid' in data:
            transaction_category_uid = data['transaction_category_uid']
        else:
            transaction_family_uid = data['transaction_family_uid']
            name = data['name']
        user_uid = request['user_uid']
        try:
            if transaction_category_uid:
                transaction_category = await request.app.storage.get_transaction_category_from_uid(transaction_category_uid)
            else:
                transaction_category = await request.app.storage.get_transaction_category_from_name(name, family_name)
            if transaction_category:
                return web.json_response(data={
                    'uid': transaction_category.uid,
                    'name': transaction_category.name,
                    'user': str(transaction_category.user),
                    'family': str(transaction_category.family)
                })
        except ValueError:
            raise
        raise web.HTTPOk
    except Exception:
        raise


@transaction_routes.get('/transaction')
async def getTransaction(request):
    raise NotImplementedError


@transaction_routes.get('/permanenttransaction')
async def getPermanentTransaction(request):
    raise NotImplementedError



#####################
# CREATE OPERATIONS #
#####################

@transaction_routes.post('/transactioncategory')
async def registerTransactionCategory(request):
    try:
        data = await request.json()
        name = data['name']
        user_uid = request['user_uid']
        transaction_family_uid = data['transaction_family_uid']
        try:
            transaction_family = await request.app.storage.get_transaction_family_from_uid(transaction_family_uid)
            # TODO: instead a creating a User object, use api get_user
            user = await request.app.storage.get_user(User(None, None, None, uid=user_uid))
        except ValueError:
            raise
        transaction_category = TransactionCategory(
            name=name,
            user=user,
            family=transaction_family
        )
        logger.debug('Trying to add {}'.format(transaction_category))
        if (await request.app.storage.get_transaction_category_from_name(transaction_category.name, transaction_category.family.uid)):
            logger.debug('{} is already used'.format(transaction_category.name))
            raise web.HTTPOk
        else:
            try:
                transaction_category = await request.app.storage.add_transaction_category(transaction_category)
            except UniqueViolation:
                pass
        raise web.HTTPOk
    except web.HTTPError:
        raise
    except Exception:
        raise


@transaction_routes.post('/transaction')
async def registerTransaction(request):
    raise NotImplementedError


@transaction_routes.post('/permanenttransaction')
async def registerPermanentTransaction(request):
    raise NotImplementedError



#####################
# UPDATE OPERATIONS #
#####################

@transaction_routes.put('/transactionfamily')
async def putTransactionFamily(request):
    raise NotImplementedError


@transaction_routes.put('/transactioncategory')
async def putTransactionCategory(request):
    raise NotImplementedError


@transaction_routes.put('/transaction')
async def putTransaction(request):
    raise NotImplementedError


@transaction_routes.put('/permanenttransaction')
async def putPermanentTransaction(request):
    raise NotImplementedError



#####################
# DELETE OPERATIONS #
#####################

@transaction_routes.delete('/transactionfamily')
async def deleteTransactionFamily(request):
    raise NotImplementedError


@transaction_routes.delete('/transactioncategory')
async def deleteTransactionCategory(request):
    raise NotImplementedError


@transaction_routes.delete('/transaction')
async def deleteTransaction(request):
    raise NotImplementedError


@transaction_routes.delete('/permanenttransaction')
async def deletePermanentTransaction(request):
    raise NotImplementedError