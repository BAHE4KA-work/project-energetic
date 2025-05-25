from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.data import DataInputScheme
import app.services.data_service as ds


router = APIRouter(prefix="/data", tags=["Данные"])


@router.post('/save_data')
async def save_raw_data(data: DataInputScheme, do_check: bool = True, session: Session = Depends(get_db)):
    try:
        await ds.save_data(data, session, do_check)
        return JSONResponse(content='Success', status_code=201)
    except Exception as e:
        return JSONResponse(content=e, status_code=400)


@router.post('/import_raw_data')
async def import_raw_data(do_check: bool = True, file: UploadFile = File(...), session: Session = Depends(get_db)):
    if file.content_type not in ("application/json",):
        raise HTTPException(status_code=400, detail="Only JSON-files are allowed")
    try:
        await ds.import_data(file, session, do_check)
        return JSONResponse(content='Success', status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
