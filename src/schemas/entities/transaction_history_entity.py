import uuid
from datetime import datetime
from typing import Optional

from pydantic import Field

from db.postgres.models.transaction_history import TransactionStatus
from schemas.entities.base_entity import BaseEntity


class TransactionHistoryEntity(BaseEntity):
    user_id: uuid.UUID
    recipient_user_id: uuid.UUID
    status: Optional[TransactionStatus] = TransactionStatus.PENDING
    amount: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
