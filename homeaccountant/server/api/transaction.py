from aiohttp import web

from homeaccountant import config
from homeaccountant.log.logger import getLogger
from homeaccountant.db.utils import TransactionFamily, TransactionCategory

logger = getLogger()

transaction_routes = web.RouteTableDef()


###################
# READ OPERATIONS #
###################

@transaction_routes.get('/transactionfamily')
async def getTransactionFamily(request):
    raise NotImplementedError


@transaction_routes.get('/transactioncategory')
async def getTransactionCategory(request):
    raise NotImplementedError


@transaction_routes.get('/transaction')
async def getTransaction(request):
    raise NotImplementedError


@transaction_routes.get('/permanenttransaction')
async def getPermanentTransaction(request):
    raise NotImplementedError



#####################
# CREATE OPERATIONS #
#####################

@transaction_routes.post('/transactionfamily')
async def registerTransactionFamily(request):
    if not config.SERVER.REGISTRATION.ALLOW:
        raise web.HTTPForbidden
    try:
        data = await request.json()
        name = data['name']
        transaction_family = TransactionFamily(
            name=name
        )
        logger.debug('Trying to add {}'.format(transaction_family))
        if (await request.app.storage.get_transaction_family(transaction_family)):
            logger.debug('{} is already used'.format(transaction_family.name))
            raise web.HTTPOk
        else:
            try:
                transaction_family = await request.app.storage.add_transaction_family(transaction_family)
            except UniqueViolation:
                pass
        raise web.HTTPOk
    except web.HTTPError as e:
        raise
    except Exception as e:
        raise


@transaction_routes.post('/transactioncategory')
async def registerTransactionCategory(request):
    if not config.SERVER.REGISTRATION.ALLOW:
        raise web.HTTPForbidden
    try:
        data = await request.json()
        name = data['name']
        user_uid = data['user_uid']
        family_name = data['family']
        try:
            transaction_family_uid = request.app.storage.get_transaction_family(family_name).uid
        except ValueError:
            raise
        transaction_category = TransactionCategory(
            name=name,
            user_uid=user_uid,
            transaction_family_uid=transaction_family_uid
        )
        logger.debug('Trying to add {}'.format(transaction_category))
        if (await request.app.storage.get_transaction_category):
            logger.debug('{} is already used'.format(transaction_family.name))
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