from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from starlette.responses import JSONResponse

from app.db.models import Event, AddressCard
from app.db.session import get_db
from app.schemas.bot import MasterAuth, EventRead, RouteResponse
from app.schemas.data import ClientCard
from app.services.bot_service import (
    authorize_master_by_code,
    mark_event_done,
    generate_route
)

router = APIRouter(prefix='/bot', tags=['Отчёты'])

@router.post("/auth", response_model=MasterAuth)
def auth_master(code: dict[str, str], session: Session = Depends(get_db)):
    master = authorize_master_by_code(session, code['code'])
    if not master:
        raise HTTPException(status_code=401, detail="Invalid authorization code")
    return MasterAuth(id=master.id, name=master.name)


@router.get("/events", response_model=List[EventRead])
def get_events_for_master(master_id: int, session: Session = Depends(get_db)):
    events = session.query(Event).filter(Event.worker_id == master_id).all()
    return events


@router.post("/events/{event_id}/done", response_model=EventRead)
def complete_event(event_id: int, master_id: dict[str, int], session: Session = Depends(get_db)):
    event = mark_event_done(session, event_id, master_id['master_id'])
    if not event:
        raise HTTPException(status_code=404, detail="Event not found or not assigned to this master")
    return event


@router.get('/address')
def get_address_card(address_card_id: int, session: Session = Depends(get_db)):
    try:
        q = session.query(AddressCard).filter_by(id=address_card_id).__dict__
        return ClientCard(**q)
    except Exception as e:
        return JSONResponse(status_code=404, content={'detail': e})


@router.post("/route", response_model=RouteResponse)
def get_route(master_lat: float, master_lon: float, dest_lat: float, dest_lon: float):
    route = generate_route(master_lat, master_lon, dest_lat, dest_lon)
    return route
