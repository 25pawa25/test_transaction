from abc import abstractmethod
from typing import Optional

from starlette.authentication import BaseUser

from repository.base.abc_entity_repository import BaseRepository
from schemas.entities.base_entity import BaseEntity


class AbstractBalanceRepository(BaseRepository):
    @abstractmethod
    async def create_user_balance(self, **fields) -> BaseEntity:
        pass

    @abstractmethod
    async def get_user_balance(self, user_id: str, raise_if_notfound: bool = True) -> Optional[BaseEntity]:
        pass

    @abstractmethod
    async def update_user_balance(self, user_id: str, **fields) -> BaseEntity:
        pass
