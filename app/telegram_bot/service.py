import httpx
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.data import ClientCard
from app.telegram_bot.config import SERVER_URL

class MasterAuthResponse(BaseModel):
    id: int
    name: str

class Event(BaseModel):
    id: int
    address_card_id: int
    type: str
    is_done: bool

async def authorize_master(code: str) -> Optional[MasterAuthResponse]:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SERVER_URL}/bot/auth", json={"code": code})
        if r.status_code == 200:
            return MasterAuthResponse(**r.json())
        return None

async def get_events(master_id: int) -> List[Event]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SERVER_URL}/bot/events", params={"master_id": master_id})
        r.raise_for_status()
        return [Event(**item) for item in r.json()]

async def mark_done(event_id: int, master_id: int) -> Event:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SERVER_URL}/bot/events/{event_id}/done", json={"master_id": master_id})
        r.raise_for_status()
        return Event(**r.json())


async def get_address_card(address_card_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SERVER_URL}/bot/address?address_card_id={address_card_id}")
        r.raise_for_status()
        return ClientCard(**r.json())


async def get_route(master_lat: float, master_lon: float, dest_lat: float, dest_lon: float) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{SERVER_URL}/bot/route", json={
            "master_lat": master_lat,
            "master_lon": master_lon,
            "dest_lat": dest_lat,
            "dest_lon": dest_lon,
        })
        r.raise_for_status()
        return r.json()
