import uuid
from decimal import Decimal

from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped

from db.postgres.models.base_model import BaseModel, Column
from db.postgres.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class UserBalance(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for user balance db table."""

    __tablename__ = "user_balance"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_balance_pkey"),
        UniqueConstraint("user_id", name="user_balance_user_id_unique"),
    )

    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), nullable=False)
    balance: Mapped[Decimal] = Column(DECIMAL(precision=12, scale=2), nullable=False, default=0.0)

    def __repr__(self):
        return (
            f"UserBalance(id={self.id}, user_id={self.user_id}, balance={self.balance})"
        )
