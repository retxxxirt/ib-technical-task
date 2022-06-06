import os
import random

from aioredis import Redis
from asyncpg import Connection

from app.schemas import Device, DeviceType, Endpoint


def is_anagrams(str_a: str, str_b: str) -> bool:
    """Check if strings are anagrams"""
    return sorted(str_a) == sorted(str_b)


async def increase_anagrams_count(redis: Redis) -> int:
    """Increase anagrams count in redis"""
    return await redis.incr("anagrams-count")


async def get_anagrams_count(redis: Redis) -> int:
    """Get anagrams count from redis"""
    return await redis.get("anagrams-count") or 0


async def create_device(database: Connection, device: Device) -> Device:
    """Save device in database"""

    device_id = await database.fetchval(
        "INSERT INTO devices(dev_id, dev_type) VALUES ($1, $2) RETURNING id",
        device.dev_id,
        device.dev_type,
    )

    device.id = device_id
    return device


async def create_random_device(database: Connection) -> Device:
    """Save random device in database"""

    dev_id = os.urandom(6).hex()
    dev_type = random.choice([t.value for t in DeviceType])
    device = Device(dev_id=dev_id, dev_type=dev_type)

    return await create_device(database, device)


async def create_endpoint(database: Connection, endpoint: Endpoint) -> Endpoint:
    """Save endpoint in database"""

    endpoint_id = await database.fetchval(
        "INSERT INTO endpoints(device_id, comment) VALUES ($1, $2) RETURNING id",
        endpoint.device_id,
        endpoint.comment,
    )

    endpoint.id = endpoint_id
    return endpoint


async def create_random_endpoint(database: Connection, device_id: int) -> Endpoint:
    """Save random endpoint with given device_id in database"""

    endpoint = Endpoint(device_id=device_id, comment="Device endpoint")
    return await create_endpoint(database, endpoint)
