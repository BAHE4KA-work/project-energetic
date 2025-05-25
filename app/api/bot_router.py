from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.models import Event, AddressCard
from app.db.session import get_db
from app.schemas.bot import MasterAuth, EventRead, RouteResponse
from app.schemas.data import ClientCard
from app.services.bot_service import authorize_master_by_code, generate_route
from app.services.event_service import complete_event as complete_event_service

router = APIRouter(prefix='/bot', tags=['Отчёты'])

@router.post("/auth", response_model=MasterAuth)
async def auth_master(code: dict[str, str], session: Session = Depends(get_db)):
    master = await authorize_master_by_code(session, code['code'])
    if not master:
        raise HTTPException(status_code=401, detail="Invalid authorization code")
    return MasterAuth(id=master.id, name=master.name)

@router.get("/events", response_model=List[EventRead])
async def get_events_for_master(master_id: int, session: Session = Depends(get_db)):
    events = session.query(Event).filter(Event.worker_id == master_id).order_by(Event.id).all()
    return events

@router.post(
    "/events/{event_id}/done",
    response_model=EventRead,
    summary="Отметить этап как выполненный и получить следующий"
)
async def complete_event(
    event_id: int,
    session: Session = Depends(get_db)
):
    current_event = session.query(Event).filter_by(id=event_id).first()
    next_event = await complete_event_service(event_id, session)
    if not next_event:
        if current_event.type == 'Контроль через месяц':
            l = session.query(Event).filter_by(worker_id=current_event.worker_id).all()
            for i in l:
                session.delete(i)
            session.commit()
            return {'result': 'success'}
        raise HTTPException(status_code=404, detail="Следующий этап не найден или цикл завершен")
    return next_event

@router.get("/address", response_model=ClientCard, summary="Получить карточку адреса по её ID")
def get_address_card(
    address_card_id: int = Query(...),
    session: Session = Depends(get_db)
):
    card = session.query(AddressCard).get(address_card_id)
    if not card:
        raise HTTPException(status_code=404, detail="AddressCard не найден")
    return card

@router.post("/route", response_model=RouteResponse)
async def get_route(master_lat: float, master_lon: float, dest_lat: float, dest_lon: float):
    route = await generate_route(master_lat, master_lon, dest_lat, dest_lon)
    return route
