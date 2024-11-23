from abc import ABC, abstractmethod

from schemas.response.balance import BalanceResponse


class AbstractBalanceService(ABC):
    @abstractmethod
    async def check_users_balance(self, user_id: str) -> BalanceResponse:
        ...

    @abstractmethod
    async def create_user_balance(self, user_id: str) -> BalanceResponse:
        ...

    @abstractmethod
    async def can_create_transaction(self, user_id: str, amount: float) -> bool:
        ...

    @abstractmethod
    async def update_user_balance(self, user_id: str, amount: float) -> BalanceResponse:
        ...
