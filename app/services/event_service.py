from typing import List, Optional, Type
from sqlalchemy.orm import Session
from app.db.models import Event

def get_all_events(session: Session) -> List[Type[Event]]:
    return session.query(Event).all()

def get_event_by_id(session: Session, event_id: int) -> Optional[Event]:
    return session.query(Event).filter(Event.id == event_id).first()

def create_event(session: Session, address_card_id: int, type: str, is_done: Optional[bool] = False, worker_id: Optional[int] = None) -> Event:
    event = Event(
        address_card_id=address_card_id,
        type=type,
        is_done=is_done,
        worker_id=worker_id
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

def update_event(session: Session, event_id: int, type: Optional[str] = None, is_done: Optional[bool] = None, worker_id: Optional[int] = None) -> Optional[Event]:
    event = get_event_by_id(session, event_id)
    if not event:
        return None
    if type is not None:
        event.type = type
    if is_done is not None:
        event.is_done = is_done
    if worker_id is not None:
        event.worker_id = worker_id
    session.commit()
    session.refresh(event)
    return event

def delete_event(session: Session, event_id: int) -> bool:
    event = get_event_by_id(session, event_id)
    if not event:
        return False
    session.delete(event)
    session.commit()
    return True
