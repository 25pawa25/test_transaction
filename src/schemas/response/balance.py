import uuid

from pydantic import BaseModel


class BalanceResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    balance: float

    class Config:
        orm_mode = True
