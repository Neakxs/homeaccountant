from aiohttp import web

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
    raise NotImplementedError


@transaction_routes.post('/transactioncategory')
async def registerTransactionCategory(request):
    raise NotImplementedError


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