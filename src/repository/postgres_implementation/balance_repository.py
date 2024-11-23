from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from common.exceptions.balance import UserBalanceNotFound, BalanceError
from db.postgres.models.balance import UserBalance
from repository.interfaces.entity.abc_balance_repository import AbstractBalanceRepository
from repository.postgres_implementation.base_repository import SQLRepository
from schemas.entities.balance_entity import BalanceEntity


class SQLBalanceRepository(SQLRepository, AbstractBalanceRepository):
    class_model = UserBalance
    entity_class = BalanceEntity

    async def create_user_balance(self, **fields) -> BalanceEntity:
        """
        Creating a user balance
        Args:
            **fields: fields of user balance
        Returns:
            user balance instance
        """
        return await self.add(self.entity_class(**fields))

    async def get_user_balance(self, user_id: str, raise_if_notfound: bool = True) -> Optional[BalanceEntity]:
        """
        Get user balance by user_id
        Args:
            user_id: id of the user
            raise_if_notfound: boolean to raise UserNotFound exception
        Returns:
            user balance instance
        """
        if balance_instance := await self.get_by(user_id=user_id):
            return self.to_entity(balance_instance)
        if raise_if_notfound:
            raise UserBalanceNotFound("User balance not found", user_id=user_id)

    async def update_user_balance(self, user_id: str, **fields) -> BalanceEntity:
        """
        Update user balance by user_id
        Args:
            user_id: id of the user
            **fields: Updated fields of UserBalance
        Returns:
            user balance instance
        """
        result = await self.session.execute(
            select(self.class_model)
            .where(self.class_model.user_id == user_id))
        if not (user_balance_db := result.unique().scalar_one_or_none()):
            raise UserBalanceNotFound("User balance not found", user_id=user_id)

        if amount := fields.pop("amount", None):
            user_balance_db.balance += Decimal(amount)

        for key, value in fields.items():
            if hasattr(user_balance_db, key):
                setattr(user_balance_db, key, value)

        try:
            await self.session.commit()
        except IntegrityError:
            raise BalanceError("Failed to update balance", user_id=user_id)

        return self.to_entity(user_balance_db)
