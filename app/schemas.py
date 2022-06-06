from enum import Enum

from pydantic import BaseModel


class CheckAnagramsRequest(BaseModel):
    str_a: str
    str_b: str


class CheckAnagramsResponse(BaseModel):
    is_anagrams: bool
    anagrams_count: int


class DeviceType(str, Enum):
    emeter = "emeter"
    zigbee = "zigbee"
    lora = "lora"
    gsm = "gsm"


class Device(BaseModel):
    id: int = None
    dev_id: str
    dev_type: DeviceType


class Endpoint(BaseModel):
    id: int = None
    device_id: int
    comment: str


class GetDevicesDataResponse(BaseModel):
    emeter_count: int
    zigbee_count: int
    lora_count: int
    gsm_count: int
