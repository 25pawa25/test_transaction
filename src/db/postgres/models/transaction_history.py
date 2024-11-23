import enum
import uuid
from decimal import Decimal

from sqlalchemy import PrimaryKeyConstraint, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped

from db.postgres.models.base_model import BaseModel, Column
from db.postgres.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


@enum.unique
class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionHistory(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for user db table."""

    __tablename__ = "transaction_history"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="transaction_history_pkey"),
    )
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), nullable=False)
    recipient_user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = Column(ENUM(TransactionStatus, name="transaction_status"), nullable=False,
                                 default=TransactionStatus.PENDING)
    amount: Mapped[Decimal] = Column(DECIMAL(precision=15, scale=2), nullable=False)

    def __repr__(self):
        return (
            f"TransactionHistory(id={self.id}, user_id={self.user_id}, recipient_user_id={self.recipient_user_id}, "
            f"status={self.status}, created_at={self.created_at}, updated_at={self.updated_at}, amount={self.amount})"
        )
