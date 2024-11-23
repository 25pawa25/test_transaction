from abc import ABC, abstractmethod
from typing import List

from schemas.request.transaction import UpdateTransactionSchema, CreateTransactionSchema, GetTransactionSchema
from schemas.response.transaction import TransactionResponse


class AbstractTransactionHistoryService(ABC):
    @abstractmethod
    async def create_transaction(self, user_id: str, schema: CreateTransactionSchema) -> TransactionResponse:
        ...

    @abstractmethod
    async def update_transaction(self, schema: UpdateTransactionSchema) -> TransactionResponse:
        ...

    @abstractmethod
    async def get_user_transactions(self, user_id: str, transaction_schema: GetTransactionSchema, **kwargs) -> List[
        TransactionResponse]:
        ...
