import uuid
from datetime import datetime

from pydantic import BaseModel

from db.postgres.models.transaction_history import TransactionStatus


class TransactionResponse(BaseModel):
    user_id: uuid.UUID
    recipient_user_id: uuid.UUID
    status: TransactionStatus
    amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
