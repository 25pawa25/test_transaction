from clients.api.v1.balance import balance_routers
from clients.api.v1.transaction_history import transaction_history_routers
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(balance_routers)
v1_router.include_router(transaction_history_routers)
