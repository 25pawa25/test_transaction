import uuid
from datetime import datetime
from typing import Iterable

from sqlalchemy import select, and_

from db.postgres.models.transaction_history import TransactionHistory
from repository.interfaces.entity.abc_transaction_history_repository import AbstractTransactionHistoryRepository
from repository.postgres_implementation.base_repository import SQLRepository
from schemas.entities.transaction_history_entity import TransactionHistoryEntity


class SQLTransactionHistoryRepository(SQLRepository, AbstractTransactionHistoryRepository):
    class_model = TransactionHistory
    entity_class = TransactionHistoryEntity

    async def create_transaction(self, **fields) -> TransactionHistoryEntity:
        """
        Creating a transaction
        Args:
            **fields: fields of transaction
        Returns:
            TransactionHistoryEntity
        """
        return await self.add(self.entity_class(**fields))

    async def update_transaction(self, transaction_id: str, **fields) -> TransactionHistoryEntity:
        """
        Updating a transaction
        Args:
            transaction_id: transaction id
            **fields: fields of transaction
        Returns:
            TransactionHistoryEntity
        """
        return await self.update(self_id=uuid.UUID(transaction_id), updated_at=datetime.utcnow(), **fields)

    async def get_user_transactions(self, user_id: str, page: int = 1, page_size: int = 10, **kwargs) -> Iterable[
        TransactionHistoryEntity]:
        """
        Get user transactions
        Args:
            user_id: id of the user
            page: number of the page
            page_size: size of the page
            **kwargs: fields to filter
        Returns:
            list of TransactionHistoryEntity
        """
        filters = [self.class_model.user_id == user_id]

        if created_at_from := kwargs.pop("created_at_from", None):
            filters.append(self.class_model.created_at >= created_at_from)
        if created_at_to := kwargs.pop("created_at_to", None):
            filters.append(self.class_model.created_at <= created_at_to)

        if updated_at_from := kwargs.pop("updated_at_from", None):
            filters.append(self.class_model.updated_at >= updated_at_from)
        if updated_at_to := kwargs.pop("updated_at_to", None):
            filters.append(self.class_model.updated_at <= updated_at_to)

        stmt = (
            select(self.class_model)
            .where(and_(*filters)).filter_by(**kwargs).limit(page_size).offset(
                (page - 1) * page_size)
        )
        result = await self.session.execute(stmt)
        return [self.to_entity(instance) for instance in result.scalars().all()]
