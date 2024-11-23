from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status, Query
from loguru import logger

from common.dependencies.auth_validation import JWTValidation
from common.exceptions.balance import LittleBalanceException
from db.postgres.models.transaction_history import TransactionStatus
from schemas.jwt_token_payload import JWTTokenPayload
from schemas.request.transaction import CreateTransactionSchema, UpdateTransactionSchema, GetTransactionSchema
from schemas.response.transaction import TransactionResponse
from services.balance.abc_balance import AbstractBalanceService
from services.transaction_history.abc_transaction_history import AbstractTransactionHistoryService

router = APIRouter(prefix="/transaction", tags=["Transaction actions"])


@router.post(
    "",
    summary="Create transaction",
    description="Create user transaction if possible",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
        request: CreateTransactionSchema,
        user_payload: JWTTokenPayload = Depends(JWTValidation()),
        transaction_service: AbstractTransactionHistoryService = Depends(),
        balance_service: AbstractBalanceService = Depends(),
) -> TransactionResponse:
    """
    Create a transaction
    Args:
        request: CreateTransactionSchema
        user_payload: jwt payload of user
        transaction_service: TransactionHistoryService
        balance_service: BalanceService
    Returns:
        TransactionResponse
    """
    logger.info(f"Create transaction by user: {user_payload.user_id}")
    if not await balance_service.can_create_transaction(user_payload.user_id, request.amount):
        raise LittleBalanceException("There is not enough money on the balance sheet.")
    instance = await transaction_service.create_transaction(user_payload.user_id, request)
    return instance


@router.get("", summary="Get user transactions", description="Get user transactions")
async def get_user_transactions(
        user_payload: JWTTokenPayload = Depends(JWTValidation()),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        status: Optional[TransactionStatus] = Query(None, description="Transaction status"),
        created_at_from: Optional[datetime] = Query(None, description="Created at from (ISO format)"),
        created_at_to: Optional[datetime] = Query(None, description="Created at to (ISO format)"),
        updated_at_from: Optional[datetime] = Query(None, description="Updated at from (ISO format)"),
        updated_at_to: Optional[datetime] = Query(None, description="Updated at to (ISO format)"),
        transaction_service: AbstractTransactionHistoryService = Depends(),
) -> List[TransactionResponse]:
    """
    Login
    Args:
        user_payload: jwt payload of user
        page: page number
        page_size: page size
        status: status of transactions to filter
        created_at_from: "created at from" to filter
        created_at_to: "created at to" to filter
        updated_at_from: "updated at from" to filter
        updated_at_to: "updated at to" to filter
        transaction_service: TransactionHistoryService
    Returns:
        List of TransactionResponse
    """
    logger.info(f"Get transactions for user: {user_payload.user_id}")
    schema = GetTransactionSchema(
        status=status,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        updated_at_from=updated_at_from,
        updated_at_to=updated_at_to,
    )
    return await transaction_service.get_user_transactions(user_payload.user_id, transaction_schema=schema, page=page,
                                                           page_size=page_size,
                                                           )


@router.patch("", summary="Update user transaction", description="Update user transaction")
async def update_user_transaction(
        request: UpdateTransactionSchema,
        user_payload: JWTTokenPayload = Depends(JWTValidation()),
        transaction_service: AbstractTransactionHistoryService = Depends(),
        balance_service: AbstractBalanceService = Depends(),
) -> TransactionResponse:
    """
    Update user transaction
    Args:
        request: UpdateTransactionSchema
        user_payload: jwt payload of user
        transaction_service: TransactionHistoryService
        balance_service: BalanceService
    Returns:
        TransactionResponse
    """
    logger.info(f"Update user transaction by user: {user_payload.user_id}; transaction: {request.transaction_id}")
    transaction = await transaction_service.update_transaction(request)
    if transaction.status == TransactionStatus.COMPLETED:
        await balance_service.update_user_balance(user_id=user_payload.user_id, amount=-transaction.amount)
        await balance_service.update_user_balance(user_id=str(transaction.recipient_user_id), amount=transaction.amount)
    return transaction
