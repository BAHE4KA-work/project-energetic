import json
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.models import RawData, AddressCard
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


async def do_check(obj: RawData, session: Session):
    card = session.query(AddressCard).filter_by(address=obj.address).first()
    if card is not None:
        return card

    card = {}

    arg = json.loads(obj.__dict__['consumption'])
    cons = []
    for k, a in arg.items():
        cons.append(a)
    card.update({'avg_cons': sum(cons) / len(cons)})
    card.update({'filling_coef': sum(cons) / len(cons) / max(cons)})

    divs = []
    for i in range(len(cons)):
        normal = 2894.53
        normal += 2.32 * obj.totalArea if obj.totalArea is not None else 0
        normal -= 177.30 * obj.residents_count if obj.residents_count is not None else 0
        if i+1 in [1, 2, 3]:
            normal -= 379.95*1.2
        elif i+1 in [4, 5, 9, 10]:
            normal -= 379.95*1.1
        else:
            normal -= 379.95
        divs.append(cons[i]/normal)
    card.update({'deviation': str(divs)[1:-1]})

    card = AddressCard()
    return ...

