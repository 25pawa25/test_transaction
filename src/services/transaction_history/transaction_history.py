from typing import List

from common.exceptions.user import UserNotExists
from repository.interfaces.entity.abc_transaction_history_repository import AbstractTransactionHistoryRepository
from repository.interfaces.grpc.abc_auth_repository import AbstractAuthRepository
from schemas.request.transaction import CreateTransactionSchema, UpdateTransactionSchema, GetTransactionSchema
from schemas.response.transaction import TransactionResponse
from services.transaction_history.abc_transaction_history import AbstractTransactionHistoryService


class TransactionHistoryService(AbstractTransactionHistoryService):
    def __init__(
            self,
            transaction_history_repository: AbstractTransactionHistoryRepository,
            auth_repository: AbstractAuthRepository,
    ) -> None:
        self.transaction_history_repository = transaction_history_repository
        self.auth_repository = auth_repository

    async def create_transaction(self, user_id: str, schema: CreateTransactionSchema) -> TransactionResponse:
        """
        Create transaction
        Args:
            user_id: user_id
            schema: CreateTransactionSchema
        Returns:
            BalanceResponse
        """
        if not await self.auth_repository.check_if_user_exists(user_id):
            raise UserNotExists("User does not exists")
        if not await self.auth_repository.check_if_user_exists(schema.recipient_user_id):
            raise UserNotExists("Recipient user does not exists")
        transaction = await self.transaction_history_repository.create_transaction(user_id=user_id, **schema.dict())
        return TransactionResponse.from_orm(transaction)

    async def update_transaction(self, schema: UpdateTransactionSchema) -> TransactionResponse:
        """
        Update user transaction by user_id
        Args:
            schema: UpdateTransactionSchema
        Returns:
            BalanceResponse
        """
        transaction = await self.transaction_history_repository.update_transaction(transaction_id=schema.transaction_id,
                                                                                   **schema.dict(
                                                                                       exclude={"transaction_id"}))
        return TransactionResponse.from_orm(transaction)

    async def get_user_transactions(self, user_id: str, transaction_schema: GetTransactionSchema, **kwargs) -> List[
        TransactionResponse]:
        """
        Get user transactions by user_id
        Args:
            user_id: id of the user
            transaction_schema: GetTransactionSchema
            **kwargs: kwargs to filter and paginate
        Returns:
            user balance instance
        """
        transactions_db = await self.transaction_history_repository.get_user_transactions(user_id=user_id,
                                                                                          **transaction_schema.dict(
                                                                                              exclude_none=True),
                                                                                          **kwargs)
        return [TransactionResponse.from_orm(transaction) for transaction in transactions_db]
