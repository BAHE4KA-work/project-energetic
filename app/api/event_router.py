from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.db.models import Master
from app.schemas.event import EventRead, EventCreate, EventUpdate
from app.services.event_service import (
    get_all_events,
    get_event_by_id,
    create_event,
    update_event,
    delete_event,
    create_initial_unassigned,
    assign_report_to_master,
)
from app.db.session import get_db

router = APIRouter(prefix="/events", tags=["Ивенты"])

@router.get("/", response_model=List[EventRead])
async def read_events(session: Session = Depends(get_db)):
    return await get_all_events(session)


@router.get("/{event_id}", response_model=EventRead)
async def read_event(event_id: int, session: Session = Depends(get_db)):
    return await get_event_by_id(session, event_id)


@router.post("/", response_model=EventRead)
async def create_new_event(data: EventCreate, session: Session = Depends(get_db)):
    return await create_event(session, data.address_card_id, data.type, data.is_done, data.worker_id)


@router.put("/{event_id}", response_model=EventRead)
async def modify_event(event_id: int, data: EventUpdate, session: Session = Depends(get_db)):
    return await update_event(session, event_id, data.type, data.is_done, data.worker_id)


@router.delete("/{event_id}")
async def remove_event(event_id: int, session: Session = Depends(get_db)):
    return await delete_event(session, event_id)


@router.post("/init_unassigned", response_model=EventRead, summary="Создать новый initial event без мастера")
async def init_unassigned(card_id: int, session: Session = Depends(get_db)):
    return await create_initial_unassigned(card_id, session)

@router.post("/assign_report/{master_id}", response_model=EventRead, summary="Назначить свободный initial event мастеру")
async def assign_report(master_id: int, session: Session = Depends(get_db)):
    master = session.query(Master).get(master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master не найден")
    ev = await assign_report_to_master(master, session)
    if not ev:
        raise HTTPException(status_code=404, detail="Нет свободных initial–ивентов")
    return ev
