from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.dependencies.registrator import add_factory_to_mapper
from db.postgres.connection import get_async_session
from repository.postgres_implementation.balance_repository import SQLBalanceRepository
from services.balance.abc_balance import AbstractBalanceService
from services.balance.balance import BalanceService


@add_factory_to_mapper(AbstractBalanceService)
def create_balance_service(
        session: AsyncSession = Depends(get_async_session),
):
    return BalanceService(
        balance_repository=SQLBalanceRepository(session=session),
    )
