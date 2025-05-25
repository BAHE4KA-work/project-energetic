from typing import List, Optional, Type
from sqlalchemy.orm import Session
from app.db.models import Event, AddressCard, Master

EVENT_SEQUENCE = [
    "Выявлены аномалии",
    "Направлено уведомление",
    "Назначена очная проверка",
    "Подтверждено нарушение",
    "Переход на другой тариф",
    "Контроль через месяц",
]

async def get_all_events(session: Session) -> List[Type[Event]]:
    return session.query(Event).all()


async def get_event_by_id(session: Session, event_id: int) -> Optional[Event]:
    return session.query(Event).filter(Event.id == event_id).first()


async def create_event(session: Session, address_card_id: int, type: str, is_done: Optional[bool] = False, worker_id: Optional[int] = None) -> Event:
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


async def update_event(session: Session, event_id: int, type: Optional[str] = None, is_done: Optional[bool] = None, worker_id: Optional[int] = None) -> Optional[Event]:
    event = await get_event_by_id(session, event_id)
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


async def delete_event(session: Session, event_id: int) -> bool:
    event = await get_event_by_id(session, event_id)
    if not event:
        return False
    session.delete(event)
    session.commit()
    return True


async def complete_event(event_id: int, session: Session) -> Optional[Event]:
    ev = session.query(Event).get(event_id)
    ev.is_done = True
    session.commit()

    idx = EVENT_SEQUENCE.index(ev.type)
    if idx + 1 < len(EVENT_SEQUENCE):
        next_type = EVENT_SEQUENCE[idx + 1]
        new_ev = Event(
            type=next_type,
            address_card_id=ev.address_card_id,
            worker_id=ev.worker_id
        )
        session.add(new_ev)
        session.commit()
        session.refresh(new_ev)
        return new_ev
    return None


async def create_initial_unassigned(card_id: int, session: Session) -> Event:
    card = session.query(AddressCard).get(card_id)
    event = Event(type=EVENT_SEQUENCE[0], address_card_id=card.id)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

async def assign_report_to_master(master: Master, session: Session) -> Optional[Event]:
    ev = (
        session.query(Event)
        .filter_by(type=EVENT_SEQUENCE[0], is_done=False, worker_id=None)
        .order_by(Event.id)
        .first()
    )
    if not ev:
        return None
    ev.worker_id = master.id
    session.commit()
    session.refresh(ev)
    return ev
