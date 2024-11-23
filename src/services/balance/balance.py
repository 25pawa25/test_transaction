from db.postgres.connection import get_postgres_session
from repository.interfaces.entity.abc_balance_repository import AbstractBalanceRepository
from repository.postgres_implementation.balance_repository import SQLBalanceRepository
from schemas.response.balance import BalanceResponse

from services.balance.abc_balance import AbstractBalanceService


class BalanceService(AbstractBalanceService):
    def __init__(
            self,
            balance_repository: AbstractBalanceRepository,
    ) -> None:
        self.balance_repository = balance_repository

    async def check_users_balance(self, user_id: str) -> BalanceResponse:
        """
        Check user balance by user_id
        Args:
            user_id: user_id
        Returns:
            BalanceResponse
        """
        balance = await self.balance_repository.get_user_balance(user_id=user_id)
        return BalanceResponse.from_orm(balance)

    async def create_user_balance(self, user_id: str) -> BalanceResponse:
        """
        create user balance
        Args:
            user_id: user_id
        Returns:
            BalanceResponse
        """
        balance = await self.balance_repository.create_user_balance(user_id=user_id)
        return BalanceResponse.from_orm(balance)

    async def can_create_transaction(self, user_id: str, amount: float) -> bool:
        """
        Check if user can create transaction
        Args:
            user_id: id of the user
            amount: amount of the transaction
        Returns:
            user balance instance
        """
        balance_instance = await self.check_users_balance(user_id=user_id)
        return balance_instance.balance - amount > 0

    async def update_user_balance(self, user_id: str, amount: float) -> BalanceResponse:
        """
        Update user balance
        Args:
            user_id: id of the user
            amount: amount of the transaction
        Returns:
            user balance instance
        """
        instance = await self.balance_repository.update_user_balance(user_id=user_id, amount=amount)
        return BalanceResponse.from_orm(instance)


async def get_balance_service():
    session = await get_postgres_session()
    return BalanceService(
        SQLBalanceRepository(session=session)
    )
