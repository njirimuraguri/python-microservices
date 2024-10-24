from pydantic import BaseModel, ConfigDict
from typing import Union


class TokenPayload(BaseModel):
    sub: Union[int | None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    email: str
    password: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: str
    password: str


# Properties to receive via API on update by User
class UserUpdate(BaseModel):
    password: Union[str | None] = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: Union[int | None] = None


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass


class UserLogin(BaseModel):
    username: str
    password: str
