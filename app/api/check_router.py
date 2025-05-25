from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.data import DataInputScheme
import app.services.check_service as cs
import app.services.data_service as ds
from app.db.models import RawData


router = APIRouter(prefix="/check", tags=["Проверки"])


@router.post('/do_plural')
async def do_plural(data: DataInputScheme, search_check: bool = True, data_id: Optional[int] = None, session: Session = Depends(get_db)):
    if data_id:
        data = session.query(RawData).filter_by(id=data_id).first()
    else:
        data = RawData(**data.__dict__)
    card, _ = await ds.create_card(data, session, do_check=False)
    our_cr: int = card.level
    try:
        res = await cs.do_plural_check(our_cr, data, search_check)
        return JSONResponse(status_code=200, content=res)
    except Exception as e:
        return HTTPException(status_code=400, detail=e)
