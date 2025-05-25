from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
    address_card_id: int
    type: str
    is_done: Optional[bool] = False
    worker_id: Optional[int] = None

class EventUpdate(BaseModel):
    type: Optional[str] = None
    is_done: Optional[bool] = None
    worker_id: Optional[int] = None

class EventRead(BaseModel):
    id: int
    address_card_id: int
    type: str
    is_done: Optional[bool]
    worker_id: Optional[int]

    class Config:
        orm_mode = True
