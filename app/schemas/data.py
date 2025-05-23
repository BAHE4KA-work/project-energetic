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
    address: str # 0

    avg_cons: float # 1
    level: Optional[int] = None # 4
    deviation: float # 3
    times_checked: int # 0
    filling_coef: float # 2
    potential_losses: float # 5
    building_type: str # 0
