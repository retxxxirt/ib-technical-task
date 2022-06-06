import aioredis
import asyncpg
from aioredis import Redis
from asyncpg import Connection

from app.settings import settings


async def get_redis() -> Redis:
    """Yield redis connection with context manager"""

    async with aioredis.from_url(settings.redis_dsn) as redis:
        yield redis


async def get_database() -> Connection:
    """Yield database connection, close it before exit"""

    database = await asyncpg.connect(settings.database_dsn)
    yield database
    await database.close()
