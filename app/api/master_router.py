from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.master import MasterCreate, MasterUpdate, MasterRead
from app.services.master_service import create_master, get_master, get_all_masters, update_master, delete_master

router = APIRouter(prefix="/admin/masters", tags=["Управление мастерами"])

@router.post("/", response_model=MasterRead)
def create_master_endpoint(data: MasterCreate, session: Session = Depends(get_db)):
    return create_master(session, name=data.name, code=data.code)

@router.get("/", response_model=List[MasterRead])
def read_masters(session: Session = Depends(get_db)):
    return get_all_masters(session)

@router.get("/{master_id}", response_model=MasterRead)
def read_master(master_id: int, session: Session = Depends(get_db)):
    master = get_master(session, master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    return master

@router.put("/{master_id}", response_model=MasterRead)
def update_master_endpoint(master_id: int, data: MasterUpdate, session: Session = Depends(get_db)):
    master = update_master(session, master_id, name=data.name, code=data.code)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    return master

@router.delete("/{master_id}", response_model=dict)
def delete_master_endpoint(master_id: int, session: Session = Depends(get_db)):
    success = delete_master(session, master_id)
    if not success:
        raise HTTPException(status_code=404, detail="Master not found")
    return {"detail": "Master deleted"}
