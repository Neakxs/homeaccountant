import abc
import asyncio


class Cache():
    @classmethod
    def create_cache(cls):
        return DefaultCache()

    @abc.abstractmethod
    async def read_variable(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    async def write_variable(self, name, value, expire=None):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_variable(self, name):
        raise NotImplementedError


class DefaultCache(Cache):
    def __init__(self):
        self.__cache = {}

    async def read_variable(self, name):
        return self.__cache[name]

    async def write_variable(self, name, value, expire=None):
        self.__cache[name] = value
        if expire:
            async def fut():
                await asyncio.sleep(expire)
                await self.delete_variable(name)
            asyncio.ensure_future(fut())
        print(self.__cache)

    async def delete_variable(self, name):
        del self.__cache[name]
