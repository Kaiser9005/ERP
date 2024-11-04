from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ActivityBase(BaseModel):
    type: str
    title: str
    description: str
    color: str

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: str
    date: datetime
    user: Optional[dict]

    class Config:
        orm_mode = True