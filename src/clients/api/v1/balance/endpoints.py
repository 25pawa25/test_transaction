from fastapi import APIRouter, Depends
from loguru import logger

from common.dependencies.auth_validation import JWTValidation
from schemas.jwt_token_payload import JWTTokenPayload
from schemas.response.balance import BalanceResponse
from services.balance.abc_balance import AbstractBalanceService

router = APIRouter(prefix="/balance", tags=["Balance actions"])


@router.get(
    "",
    summary="Get user balance",
    description="Get user balance",
    response_model=BalanceResponse
)
async def get_user_balance(
    user_payload: JWTTokenPayload = Depends(JWTValidation()),
    balance_service: AbstractBalanceService = Depends(),
):
    """
    Registers a new user in the system
    Args:
        user_payload: jwt payload of user
        balance_service: BalanceService
    Returns:
        BalanceResponse
    """
    logger.info(f"Check balance by user: {user_payload.user_id}")
    return await balance_service.check_users_balance(user_payload.user_id)
