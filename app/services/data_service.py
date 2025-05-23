import json
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.models import RawData
from app.schemas.data import DataInputScheme


async def save_data(data: DataInputScheme, session: Session) -> None:
    new_data = {}
    for key, arg in data.__dict__.items():
        if key == 'consumption':
            new_data.update({key: ''.join(str(arg).replace('\'', '\"'))})
        elif key == 'residentsCount':
            new_data.update({'residents_count': arg})
        else:
            new_data.update({key: arg})
    object = RawData(**new_data)
    session.add(object)
    session.commit()


async def import_data(file: UploadFile, session: Session):
    raw = await file.read()
    text = raw.decode("utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = []
        for ln in text.splitlines():
            if not ln.strip():
                continue
            data.append(json.loads(ln))

    parsed: List[DataInputScheme] = []
    for item in data:
        obj = DataInputScheme(**item)
        parsed.append(obj)

    for p in parsed:
        await save_data(p, session)
