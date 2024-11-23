import uuid
from typing import Optional

from schemas.entities.base_entity import BaseEntity


class BalanceEntity(BaseEntity):
    user_id: uuid.UUID
    balance: Optional[float]

    class Config:
        orm_mode = True
