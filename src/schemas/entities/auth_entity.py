from pydantic.main import BaseModel


class AuthEntity(BaseModel):
    user_id: str
    is_superuser: bool = False


class RefreshEntity(AuthEntity):
    refresh_token: str
