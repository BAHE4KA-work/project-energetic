from sqlalchemy.orm import Session
from typing import Optional, List, Type
from app.db.models import Master, Event


def authorize_master_by_code(session: Session, code: str) -> Optional[Master]:
    return session.query(Master).filter(Master.code == code).first()


def get_events_for_master(session: Session, master_id: int) -> List[Type[Event]]:
    return session.query(Event).filter(Event.worker_id == master_id).order_by(Event.id).all()


def mark_event_done(session: Session, event_id: int, master_id: int) -> Optional[Event]:
    event = session.query(Event).filter(Event.id == event_id, Event.worker_id == master_id).first()
    if event:
        event.is_done = True
        session.commit()
        session.refresh(event)
    return event

# Инициация цепочки событий (плана отчёта)
def initiate_check(address_card_id: int, session: Session, master_id: Optional[int] = None) -> List[Event]:
    stages = [
        "Выявлены аномалии",
        "Направлено уведомление",
        "Назначена очная проверка",
        "Подтверждено нарушение",
        "Переход на другой тариф",
        "Контроль через месяц",
    ]
    created_events = []
    for stage in stages:
        event = Event(
            address_card_id=address_card_id,
            type=stage,
            is_done=False,
            worker_id=master_id
        )
        session.add(event)
        created_events.append(event)
    session.commit()
    for event in created_events:
        session.refresh(event)
    return created_events


def generate_route(master_lat: float, master_lon: float, dest_lat: float, dest_lon: float) -> dict:
    # Тут заглушка, позже подключим внешний сервис маршрутизации
    return {
        "start": {"lat": master_lat, "lon": master_lon},
        "end": {"lat": dest_lat, "lon": dest_lon},
        "route": [
            {"lat": master_lat, "lon": master_lon},
            {"lat": dest_lat, "lon": dest_lon}
        ],
        "distance_km": 5.0  # пример
    }
