from pydantic import BaseModel
from typing import List

class MasterAuth(BaseModel):
    id: int
    name: str

class EventRead(BaseModel):
    id: int
    address_card_id: int
    type: str
    is_done: bool

    class Config:
        orm_mode = True

class LocationInput(BaseModel):
    master_lat: float
    master_lon: float
    dest_lat: float
    dest_lon: float

class RouteStep(BaseModel):
    lat: float
    lon: float

class RouteResponse(BaseModel):
    start: RouteStep
    end: RouteStep
    route: List[RouteStep]
    distance_km: float
