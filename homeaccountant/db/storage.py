import abc
import copy
import asyncio
import sqlalchemy as sa

from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.orm import sessionmaker
from aiopg.sa import create_engine

from homeaccountant import config
from homeaccountant.db.utils import User, TransactionFamily, TransactionCategory, Account
from homeaccountant.db.tables import UserSQL, TransactionFamilySQL, TransactionCategorySQL, AccountSQL


SQL_TABLES = [UserSQL, TransactionFamilySQL, TransactionCategorySQL, AccountSQL]
DEFAULT_FAMILIES = [
    {'name':'Family 1', 'uid': 1},
    {'name':'Family 2', 'uid': 2},
    {'name':'Family 3', 'uid': 3},
    {'name':'Others', 'uid': 4}
]

async def get_object_from(engine, table, dataclass, accessors, values, with_user_uid=False, user_uid=None):
    async with engine.acquire() as conn:
        query = table.c[accessors[0]] == values[0]
        for i in range(1, len(accessors)):
            query = (query) & (table.c[accessors[i]] == values[i])
        print(query)
        if with_user_uid:
            query = (query) & (table.c['user_uid'] == user_uid)
        resp = await conn.execute(table.select().where(query))
        try:
            r = await resp.fetchone()
            if r:
                fields = dataclass.__annotations__
                for index, value in enumerate(fields):
                    fields[value] = r[index]
                print(fields)
                return dataclass(**fields)
            else:
                return None
        except TypeError:
            return None

class Storage:
    def __init__(self):
        self._engine = None

    async def add_user(self, user):
        async with self._engine.acquire() as conn:
            resp = await conn.execute(UserSQL.insert().values(email=user.email, password_salt=user.password_salt, password_hash=user.password_hash))
            user.uid = (await resp.fetchone())[0]
            return user

    async def get_user(self, user):
        async with self._engine.acquire() as conn:
            if user.uid:
                resp = await conn.execute(UserSQL.select().where(UserSQL.c.uid == user.uid))
            elif user.email:
                resp = await conn.execute(UserSQL.select().where(UserSQL.c.email == user.email))
            else:
                return None
            try:
                r = await resp.fetchone()
                return User(**{
                    'uid': r[0],
                    'email': r[1],
                    'display_name': r[2],
                    'password_salt': r[3],
                    'password_hash': r[4],
                    'enabled': r[5]
                })
            except TypeError:
                return None
    
    async def add_account(self, account):
        async with self._engine.acquire() as conn:
            resp = await conn.execute(AccountSQL.insert().values(name=account.name, balance=account.balance, acronym=account.acronym, user_uid=account.user.uid))
            account.uid = (await resp.fetchone())[0]
            return account
    
    async def get_account_from_uid(self, account_uid, user_uid):
        return await get_object_from(
            engine=self._engine,
            table=AccountSQL,
            dataclass=Account,
            accessors=["uid"],
            values=[account_uid],
            with_user_uid=True,
            user_uid=user_uid
        )

    async def get_account_from_name(self, account_name, user_uid):
        return await get_object_from(
            engine=self._engine,
            table=AccountSQL,
            dataclass=Account,
            accessors=["name"],
            values=[account_name],
            with_user_uid=True,
            user_uid=user_uid
        )

    async def get_account_from_acronym(self, account_acronym, user_uid):
        return await get_object_from(
            engine=self._engine,
            table=AccountSQL,
            dataclass=Account,
            accessors=["acronym"],
            values=[account_acronym],
            with_user_uid=True,
            user_uid=user_uid
        )

    async def get_accounts(self, user):
        raise NotImplementedError

    async def get_transaction_family_from_uid(self, transaction_family_uid):
        return await get_object_from(
            engine=self._engine,
            table=TransactionFamilySQL,
            dataclass=TransactionFamily,
            accessors=["uid"],
            values=[transaction_family_uid],
            with_user_uid=False
        )
    
    async def add_transaction_category(self, transaction_category):
        async with self._engine.acquire() as conn:
            resp = await conn.execute(TransactionCategorySQL.insert().values(name=transaction_category.name, user_uid=transaction_category.user.uid, transaction_family_uid=transaction_category.family.uid))
            transaction_category.uid = (await resp.fetchone())[0]
            return transaction_category

    async def get_transaction_category_from_uid(self, transaction_category_uid):
        return await get_object_from(
            engine=self._engine,
            table=TransactionCategorySQL,
            dataclass=TransactionCategory,
            accessors=["uid"],
            values=[transaction_category_uid],
            with_user_uid=False
        )

    async def get_transaction_category_from_name(self, name, transaction_family_uid):
        return await get_object_from(
            engine=self._engine,
            table=TransactionCategorySQL,
            dataclass=TransactionCategory,
            accessors=["name", "transaction_family_uid"],
            values=[name, transaction_family_uid],
            with_user_uid=False
        )

    async def close(self):
        try:
            self._engine.close()
            await self._engine.wait_closed()
        except AttributeError:
            pass

    async def __initialize(self):
        self._engine = await self._create_engine()
        await self.__init_tables()

    @abc.abstractmethod
    async def _create_engine(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_existing_tables(self, conn):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_existing_families(self, conn):
        raise NotImplementedError

    @classmethod
    async def open_storage(cls):
        storage = PostgresStorage()
        await storage.__initialize()
        return storage

    async def __init_tables(self):
        async with self._engine.acquire() as conn:
            Session = sessionmaker(bind=conn)
            session = Session()
            existing_tables = {i[0] for i in (await (await self._get_existing_tables(conn)).fetchall())}
            for table in SQL_TABLES:
                if str(table) not in existing_tables:
                    await conn.execute(CreateTable(table))
            existing_families = {i[0] for i in (await (await self._get_existing_families(conn)).fetchall())}
            for family in DEFAULT_FAMILIES:
                if family['uid'] not in existing_families:
                    await conn.execute(TransactionFamilySQL.insert().values(**family))


class PostgresStorage(Storage):
    async def _create_engine(self):
        return await create_engine(
            user=config.DATABASE.POSTGRES.USERNAME,
            password=config.DATABASE.POSTGRES.PASSWORD,
            database=config.DATABASE.POSTGRES.DATABASE,
            host=config.DATABASE.POSTGRES.HOSTNAME,
            port=config.DATABASE.POSTGRES.PORT
        )

    async def _get_existing_tables(self, conn):
        return await conn.execute(
            "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")

    async def _get_existing_families(self, conn):
        return await conn.execute(
            'SELECT * FROM "TRANSACTION_FAMILY";' 
        )


async def main():
    store = await Storage.open_storage()
    await store.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
