from functools import lru_cache
from typing import Optional

import grpc
from loguru import logger

from clients.grpc.proto.transaction import transaction_pb2
from clients.grpc.proto.transaction.transaction_pb2_grpc import TransactionServicer
from services.balance.abc_balance import AbstractBalanceService
from services.balance.balance import get_balance_service


class TransactionServicer(TransactionServicer):
    def __init__(self):
        self.balance_service: Optional[AbstractBalanceService] = None

    async def init_services(self):
        self.balance_service = await get_balance_service()

    async def CreateUserBalance(self, request, context) -> transaction_pb2.CreateUserBalanceResponse:
        """
        GRPC create user balance
        Args:
            request: GRPC request object
            context: GRPC context object for response
        Returns:
            CreateUserBalanceResponse
            context INTERNAL if error in service working
        """
        try:
            user_balance = await self.balance_service.create_user_balance(request.user_id)
            return transaction_pb2.CreateUserBalanceResponse(id=str(user_balance.id))
        except Exception as e:
            error_msg = "Error occurred: " + str(e)
            context.set_details(error_msg)
            logger.opt(exception=e).error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)


@lru_cache
async def get_transaction_servicer():
    servicer = TransactionServicer()
    await servicer.init_services()
    return servicer
