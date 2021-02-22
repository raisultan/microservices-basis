from typing import Optional

from pydantic import BaseModel


class UserLoginForm(BaseModel):
    email: str
    password: str


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RefreshToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'
