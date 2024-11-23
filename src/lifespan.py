import contextlib
from typing import AsyncIterator

from core.config import settings
from db.postgres.session_manager import db_manager
from fastapi import FastAPI


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_manager.init(settings.postgres.database_url)
    yield
    await db_manager.close()
