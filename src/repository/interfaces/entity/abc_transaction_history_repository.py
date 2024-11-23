from abc import abstractmethod
from typing import Optional

from repository.base.abc_entity_repository import BaseRepository
from schemas.entities.base_entity import BaseEntity


class AbstractTransactionHistoryRepository(BaseRepository):
    @abstractmethod
    async def create_transaction(self, **fields) -> BaseEntity:
        pass

    @abstractmethod
    async def update_transaction(self, transaction_id: str, **fields) -> Optional[BaseEntity]:
        pass

    @abstractmethod
    async def get_user_transactions(self, user_id: str, page: int = 1, page_size: int = 10, **kwargs) -> Optional[
        BaseEntity]:
        pass
