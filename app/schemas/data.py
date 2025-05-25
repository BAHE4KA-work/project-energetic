from pydantic import BaseModel as base
from typing import Optional, List


class DataInputScheme(base):
    accountId: int
    isCommercial: bool
    address: str
    buildingType: str
    roomsCount: Optional[int] = None
    residentsCount: Optional[int] = None
    totalArea: Optional[float] = None
    consumption: dict | str

    class Config:
        validate_by_name = True


class FilterInput(base):
    street: Optional[str] = None
    category: Optional[bool] = None
    inspected: Optional[bool] = None


class ClientCard(base):
    address: Optional[str] = None

    avg_cons: Optional[float] = None
    level: Optional[int] = None
    deviation: Optional[str] = None
    times_checked: Optional[int] = None
    filling_coef: Optional[float] = None
    potential_losses: Optional[float] = None
    building_type: Optional[str] = None


class AddressFilter(base):
    city: Optional[str] = None
    street: Optional[str] = None


class RiskLevelFilter(base):
    level: Optional[int] = None  # 0 - нормальный, 1 - желтый, 2 - красный


class EventSchema(base):
    id: int
    address_card_id: int
    type: str
    is_done: bool
    worker_id: Optional[int]

    class Config:
        orm_mode = True


class ReportSchema(base):
    address_card_id: int
    events: List[EventSchema]
