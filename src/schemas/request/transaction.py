from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from db.postgres.models.transaction_history import TransactionStatus


class CreateTransactionSchema(BaseModel):
    recipient_user_id: str
    amount: float


class UpdateTransactionSchema(BaseModel):
    transaction_id: str
    status: TransactionStatus


class GetTransactionSchema(BaseModel):
    status: Optional[TransactionStatus]
    created_at_from: Optional[datetime]
    created_at_to: Optional[datetime]
    updated_at_from: Optional[datetime]
    updated_at_to: Optional[datetime]
