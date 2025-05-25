import json
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.models import RawData, AddressCard
from app.schemas.data import DataInputScheme
from app.services.check_service import do_plural_check
from app.services.event_service import create_initial_unassigned


async def save_data(data: DataInputScheme, session: Session, do_check: bool = True):
    new_data = {}
    for key, arg in data.__dict__.items():
        if key == 'consumption':
            new_data.update({key: ''.join(str(arg).replace('\'', '\"'))})
        elif key == 'residentsCount':
            new_data.update({'residents_count': arg})
        else:
            new_data.update({key: arg})
    obj = RawData(**new_data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return await create_card(obj, session, do_check)


async def import_data(file: UploadFile, session: Session, do_check: bool = True):
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

    c = [0, 0]
    for item in data:
        _, res = await save_data(DataInputScheme(**item), session, do_check)
        if res == item['isCommercial']:
            c[1] += 1
        c[0] += 1

        if c[0] >= 50:
            print(c)
            break
    return c


async def create_card(obj: RawData, session: Session, do_check: bool = True):
    card: Optional[AddressCard] = session.query(AddressCard).filter_by(address=obj.address).first()
    if card is not None:
        return card

    card: dict = {}
    card.update({'address': obj.address, 'times_checked': 0, 'building_type': obj.buildingType})

    arg = json.loads(obj.__dict__['consumption'])
    cons = []
    for k, a in arg.items():
        cons.append(a)
    card.update({'avg_cons': sum(cons) / len(cons)})
    try:
        card.update({'filling_coef': sum(cons) / len(cons) / max(cons)})
    except ZeroDivisionError:
        card.update({'filling_coef': 0})

    divs = []
    for i in range(len(cons)):
        normal = 50
        normal += 1.2 * obj.totalArea if obj.totalArea is not None else 0
        normal += 30 * obj.residents_count if obj.residents_count is not None else 0
        if i+1 in [1, 2, 3]:
            normal = normal*1.2
        elif i+1 in [4, 5, 9, 10]:
            normal = normal*1.1
        divs.append(cons[i]/normal)
    card.update({'deviation': str(divs)[1:-1]})

    y = 0
    r = 0
    for d in divs:
        if 1.2 <= d <= 1.6:
            y += 1
        elif d > 1.6:
            r += 1

    level: int = 0
    if r >= 6:
        level = 2
    elif y >= 6 or y+r >= 6:
        level = 1

    card.update({'level': level, 'potential_losses': sum(cons)*(sum(divs)-1*len(divs))*4.5})

    card: AddressCard = AddressCard(**card)
    session.add(card)
    session.commit()
    session.refresh(card)
    res = None
    if do_check:
        res = await do_plural_check(level, obj)
    if res:
        await create_initial_unassigned(card.id, session)
    return card, res


async def get_cards_by_address_filter(session: Session, city: str | None = None, street: str | None = None):
    query = session.query(AddressCard)
    if city:
        query = query.filter(AddressCard.address.ilike(f'%{city}%'))
    if street:
        query = query.filter(AddressCard.address.ilike(f'%{street}%'))
    return query.all()


async def get_cards_by_risk_level(session: Session, level: int):
    return session.query(AddressCard).filter(AddressCard.level == str(level)).all()

