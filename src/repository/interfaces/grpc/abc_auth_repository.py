from abc import ABC, abstractmethod


class AbstractAuthRepository(ABC):
    @abstractmethod
    async def check_if_user_exists(self, user_id: str):
        pass
