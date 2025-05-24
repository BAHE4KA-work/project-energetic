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
    level: int
    deviation: str
    times_checked: int
    filling_coef: float
    potential_losses: float
    building_type: str
#
# class CheckDataFrame(base):
#     accountId: int
#     isCommercial: Optional[bool] = None
#     address: str
#     buildingType: str
#     roomsCount: Optional[int] = None
#     residents_count: Optional[int] = None
#     totalArea: Optional[float] = None
#
#     consumption_1: Optional[int] = None
#     consumption_2: Optional[int] = None
#     consumption_3: Optional[int] = None
#     consumption_4: Optional[int] = None
#     consumption_5: Optional[int] = None
#     consumption_6: Optional[int] = None
#     consumption_7: Optional[int] = None
#     consumption_8: Optional[int] = None
#     consumption_9: Optional[int] = None
#     consumption_10: Optional[int] = None
#     consumption_11: Optional[int] = None
#     consumption_12: Optional[int] = None
