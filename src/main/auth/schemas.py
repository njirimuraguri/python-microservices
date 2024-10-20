from pydantic import BaseModel
from typing import Union


class TokenPayload(BaseModel):
    sub: Union[int | None] = None


class Token(BaseModel):
    access_token: str
    token_type: str
