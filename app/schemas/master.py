from pydantic import BaseModel
from typing import Optional

class MasterCreate(BaseModel):
    name: str
    code: str

class MasterUpdate(BaseModel):
    name: Optional[str]
    code: Optional[str]

class MasterRead(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        orm_mode = True
