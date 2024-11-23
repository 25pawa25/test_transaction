from pydantic import BaseModel


class JWTTokenPayload(BaseModel):
    user_id: str
    is_superuser: bool
