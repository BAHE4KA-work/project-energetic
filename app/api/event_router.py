from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.event import EventCreate, EventUpdate, EventRead
from app.services.event_service import get_all_events, get_event_by_id, create_event, update_event, delete_event
from app.db.session import get_db

router = APIRouter(prefix="/events", tags=["Ивенты"])

@router.get("/", response_model=List[EventRead])
def read_events(session: Session = Depends(get_db)):
    return get_all_events(session)

@router.get("/{event_id}", response_model=EventRead)
def read_event(event_id: int, session: Session = Depends(get_db)):
    event = get_event_by_id(session, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/", response_model=EventRead)
def create_new_event(event_in: EventCreate, session: Session = Depends(get_db)):
    return create_event(
        session,
        address_card_id=event_in.address_card_id,
        type=event_in.type,
        is_done=event_in.is_done,
        worker_id=event_in.worker_id
    )

@router.put("/{event_id}", response_model=EventRead)
def update_existing_event(event_id: int, event_in: EventUpdate, session: Session = Depends(get_db)):
    event = update_event(
        session,
        event_id,
        type=event_in.type,
        is_done=event_in.is_done,
        worker_id=event_in.worker_id
    )
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/{event_id}", response_model=dict)
def delete_existing_event(event_id: int, session: Session = Depends(get_db)):
    success = delete_event(session, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"detail": "Event deleted"}
