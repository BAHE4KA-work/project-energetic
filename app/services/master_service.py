from typing import Optional, List, Type
from sqlalchemy.orm import Session

from app.db.models import Master

async def create_master(session: Session, name: str, code: str) -> Master:
    master = Master(name=name, code=code)
    session.add(master)
    session.commit()
    session.refresh(master)
    return master

async def get_master(session: Session, master_id: int) -> Optional[Master]:
    return session.query(Master).filter(Master.id == master_id).first()

async def get_all_masters(session: Session) -> List[Type[Master]]:
    return session.query(Master).all()

async def update_master(session: Session, master_id: int, name: Optional[str] = None, code: Optional[str] = None) -> Optional[Type[Master]]:
    master = session.query(Master).filter(Master.id == master_id).first()
    if not master:
        return None
    if name is not None:
        master.name = name
    if code is not None:
        master.code = code
    session.commit()
    session.refresh(master)
    return master

async def delete_master(session: Session, master_id: int) -> bool:
    master = session.query(Master).filter(Master.id == master_id).first()
    if not master:
        return False
    session.delete(master)
    session.commit()
    return True
