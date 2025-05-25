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
