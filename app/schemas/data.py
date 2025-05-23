from pydantic import BaseModel as base
from typing import Optional


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
    address: str

    avg_cons: float
    level: Optional[int] = None # 4
    deviation: float
    times_checked: int
    filling_coef: float
    potential_losses: float # 5
    building_type: str
