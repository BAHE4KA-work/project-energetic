import io
import xlsxwriter
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.db.session import get_db
from app.schemas.data import DataInputScheme, AddressFilter
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


@router.post('/filter_by_address')
async def filter_cards_by_address(filter: AddressFilter, session: Session = Depends(get_db)):
    cards = await ds.get_cards_by_address_filter(session, city=filter.city, street=filter.street)
    if not cards:
        raise HTTPException(status_code=404, detail="Данные по заданному фильтру не найдены")
    return cards

@router.get('/red_violations')
async def get_red_violations(session: Session = Depends(get_db)):
    cards = await ds.get_cards_by_risk_level(session, level=2)
    if not cards:
        raise HTTPException(status_code=404, detail="Нет красных нарушений")
    return cards

@router.get('/yellow_violations')
async def get_yellow_violations(session: Session = Depends(get_db)):
    cards = await ds.get_cards_by_risk_level(session, level=1)
    if not cards:
        raise HTTPException(status_code=404, detail="Нет подозрительных отклонений")
    return cards

@router.get(
    "/export_excel",
    summary="Экспорт всех таблиц базы в файл Excel (XLSX)"
)
def export_all_tables_excel(session: Session = Depends(get_db)):
    engine = session.get_bind()
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for name in table_names:
            try:
                df = pd.read_sql_table(name, con=engine)
            except ValueError:
                df = pd.read_sql_query(f"SELECT * FROM {name}", con=engine)
            df.to_excel(writer, sheet_name=name[:31], index=False)
    output.seek(0)

    headers = {
        "Content-Disposition": 'attachment; filename="all_tables_export.xlsx"'
    }
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )
