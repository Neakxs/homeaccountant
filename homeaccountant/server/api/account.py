from aiohttp import web

account_routes = web.RouteTableDef()


###################
# READ OPERATIONS #
###################

@account_routes.get('/account')
async def getAccount(request):
    raise NotImplementedError



#####################
# CREATE OPERATIONS #
#####################

@account_routes.post('/account')
async def registerAccount(request):
    raise NotImplementedError



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