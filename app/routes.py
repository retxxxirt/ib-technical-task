from aioredis import Redis
from asyncpg import Connection
from fastapi import APIRouter, Depends, Body
from starlette import status

from app import services
from app.deps import get_redis, get_database
from app.schemas import CheckAnagramsRequest, CheckAnagramsResponse, GetDevicesDataResponse

router = APIRouter()


@router.post("/check-anagrams", response_model=CheckAnagramsResponse)
async def check_anagrams(redis: Redis = Depends(get_redis), data: CheckAnagramsRequest = Body()):
    """Checks if strings are anagrams"""

    if is_anagrams := services.is_anagrams(data.str_a, data.str_b):
        anagrams_count = await services.increase_anagrams_count(redis)
    else:
        anagrams_count = await services.get_anagrams_count(redis)

    return CheckAnagramsResponse(
        is_anagrams=is_anagrams,
        anagrams_count=anagrams_count,
    )


@router.post("/create-devices", status_code=status.HTTP_201_CREATED)
async def create_devices(database: Connection = Depends(get_database)):
    """Creates 10 random devices, and 5 random endpoints for these devices"""

    async with database.transaction():
        devices = []

        for _ in range(10):
            device = await services.create_random_device(database)
            devices.append(device)

        for device in devices[:5]:
            await services.create_random_endpoint(database, device.id)


@router.get("/get-devices-data", response_model=GetDevicesDataResponse)
async def get_devices_data(database: Connection = Depends(get_database)):
    """Getting amount of devices without endpoints, grouped by device type"""

    result = await database.fetchrow(
        """ 
        SELECT count(d) FILTER ( WHERE d.dev_type = 'emeter' ) emeter_count,
           count(d) FILTER ( WHERE d.dev_type = 'zigbee' ) zigbee_count,
           count(d) FILTER ( WHERE d.dev_type = 'lora' )   lora_count,
           count(d) FILTER ( WHERE d.dev_type = 'gsm' )    gsm_count
        FROM devices d
                 LEFT OUTER JOIN endpoints e ON d.id = e.device_id
        WHERE e IS NULL"""
    )

    return GetDevicesDataResponse(**dict(result.items()))
