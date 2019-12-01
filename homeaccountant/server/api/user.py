from aiohttp import web

user_routes = web.RouteTableDef()

@user_routes.get('/user')
async def getUser(request):
    pass

@user_routes.put('/user')
async def putUser(request):
    pass

@user_routes.post('/user/register')
async def registerUser(request):
    pass

@user_routes.get('/user/confirm')
async def confirmUser(request):
    pass

@user_routes.get('/user/login')
async def loginUser(request):
    pass

@user_routes.get('/user/logout')
async def logoutUser(request):
    pass