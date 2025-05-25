from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.event import MasterAuth, EventRead, RouteResponse
from app.services.event_service import (
    authorize_master_by_code,
    get_events_for_master,
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
def fetch_plan(master_id: int, session: Session = Depends(get_db)):
    events = get_events_for_master(session, master_id)
    return events

@router.post("/events/{event_id}/done", response_model=EventRead)
def complete_event(event_id: int, master_id: int, session: Session = Depends(get_db)):
    event = mark_event_done(session, event_id, master_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found or not assigned to this master")
    return event

@router.post("/route", response_model=RouteResponse)
def get_route(master_lat: float, master_lon: float, dest_lat: float, dest_lon: float):
    route = generate_route(master_lat, master_lon, dest_lat, dest_lon)
    return route
