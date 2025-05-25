from fastapi import HTTPException
from scipy.integrate import tplquad
from sqlalchemy.orm import Session
from typing import Optional, List, Type
from app.db.models import Master, Event
from app.services.event_service import complete_event


async def authorize_master_by_code(session: Session, code: str) -> Optional[Master]:
    return session.query(Master).filter(Master.code == code).first()


async def get_events_for_master(master_id: int, session: Session) -> List[Type[Event]]:
    return (
        session.query(Event)
        .filter_by(worker_id=master_id, is_done=False)
        .order_by(Event.id)
        .all()
    )


async def mark_event_done(event_id: int, session: Session) -> Optional[Event]:
    new_event = await complete_event(event_id, session)
    if new_event is None:
        raise HTTPException(status_code=404, detail="Следующий этап не найден или цикл завершен")
    if type(new_event) is dict:
        return new_event['result']
    return new_event


async def generate_route(master_lat: float, master_lon: float, dest_lat: float, dest_lon: float) -> dict:
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
