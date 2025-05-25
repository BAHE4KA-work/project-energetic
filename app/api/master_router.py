from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.master import MasterCreate, MasterUpdate, MasterRead
from app.services.master_service import create_master, get_master, get_all_masters, update_master, delete_master

router = APIRouter(prefix="/admin/masters", tags=["Управление мастерами"])

@router.post("/", response_model=MasterRead)
async def create_master_endpoint(data: MasterCreate, session: Session = Depends(get_db)):
    return await create_master(session, name=data.name, code=data.code)

@router.get("/", response_model=List[MasterRead])
async def read_masters(session: Session = Depends(get_db)):
    return await get_all_masters(session)

@router.get("/{master_id}", response_model=MasterRead)
async def read_master(master_id: int, session: Session = Depends(get_db)):
    master = await get_master(session, master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    return master

@router.put("/{master_id}", response_model=MasterRead)
async def update_master_endpoint(master_id: int, data: MasterUpdate, session: Session = Depends(get_db)):
    master = await update_master(session, master_id, name=data.name, code=data.code)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    return master

@router.delete("/{master_id}", response_model=dict)
async def delete_master_endpoint(master_id: int, session: Session = Depends(get_db)):
    success = await delete_master(session, master_id)
    if not success:
        raise HTTPException(status_code=404, detail="Master not found")
    return {"detail": "Master deleted"}
