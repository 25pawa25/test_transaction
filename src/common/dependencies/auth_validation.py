from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader, HTTPBearer
from loguru import logger
from pydantic import ValidationError

from common.exceptions.validation import InvalidTokenException
from core.config import settings
from schemas.jwt_token_payload import JWTTokenPayload

api_key_header = APIKeyHeader(name="Authorization", scheme_name="Bearer", auto_error=False)


class JWTValidation(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[JWTTokenPayload]:
        try:
            credentials = await super().__call__(request)
            if not credentials:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized!")
            token = credentials.credentials
            decoded_token: dict = jwt.decode(
                token, settings.jwt.jwt_secret_key, algorithms=[settings.jwt.encode_algorithm]
            )
            payload = JWTTokenPayload(**decoded_token)
            return payload
        except (
                HTTPException,
                jwt.DecodeError,
                jwt.InvalidKeyError,
                jwt.InvalidIssuerError,
                jwt.InvalidSignatureError,
                jwt.exceptions.ExpiredSignatureError,
                ValidationError,
        ) as e:
            logger.error("Can't decode jwt token!")
            message = "Token is invalid or expired"
            if not isinstance(e, HTTPException):
                message = f"Token is invalid or expired! See {token}"
            raise InvalidTokenException(message)


class JWTAdminValidation:
    async def __call__(self, auth_data: JWTTokenPayload = Depends(JWTValidation())) -> JWTTokenPayload:
        if not (auth_data and not auth_data.is_superuser or settings.project.debug):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return auth_data
