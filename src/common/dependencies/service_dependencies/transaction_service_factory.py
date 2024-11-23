from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.dependencies.registrator import add_factory_to_mapper
from db.postgres.connection import get_async_session
from repository.grpc_implementation.auth_repository import get_grpc_auth_repository
from repository.postgres_implementation.transaction_history_repository import SQLTransactionHistoryRepository
from services.transaction_history.abc_transaction_history import AbstractTransactionHistoryService
from services.transaction_history.transaction_history import TransactionHistoryService


@add_factory_to_mapper(AbstractTransactionHistoryService)
def create_transaction_service(
        session: AsyncSession = Depends(get_async_session),
):
    return TransactionHistoryService(
        transaction_history_repository=SQLTransactionHistoryRepository(session=session),
        auth_repository=get_grpc_auth_repository()
    )
