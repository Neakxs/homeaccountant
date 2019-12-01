import abc


class Cache():
    @classmethod
    def create_cache(cls):
        return DefaultCache()

    @abc.abstractmethod
    async def read_variable(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    async def write_variable(self, name, value):
        raise NotImplementedError


class DefaultCache(Cache):
    def __init__(self):
        self.__cache = {}

    async def read_variable(self, name):
        return self.__cache[name]

    async def write_variable(self, name, value):
        self.__cache[name] = value
