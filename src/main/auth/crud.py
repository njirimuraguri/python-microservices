from typing import Any, Union, Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import select

from . import model as user_model, schema as user_schema
from ..database.base import Base
from .model import User
from .jwt_security import verify_password, get_password_hash

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDUser(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def create_user(
            self, async_db: AsyncSession, *, obj_in: Union[user_schema.UserCreate, dict[str, Any]]
    ) -> user_model.User:
        user_data = obj_in.model_dump(exclude_unset=True)
        if user_data.get("password"):
            user_data["password"] = get_password_hash(user_data["password"])

        db_user = self.model(**user_data)
        async_db.add(db_user)
        await async_db.commit()
        await async_db.refresh(db_user)
        return db_user

    # function to get a user
    async def get_user(self, async_db: AsyncSession, user_id: int) -> [ModelType]:
        user = await async_db.execute(select(self.model).where(self.model.id == user_id))
        return list(user.scalars().all())

    # function to get users
    async def get_users(self, async_db: AsyncSession, skip: int = 0, limit: int = 100) -> list[user_model.User]:
        users = await async_db.execute(select(self.model).offset(skip).limit(limit))
        return list(users.scalars().all())

    # get a user by email
    async def get_user_by_email(self, async_db: AsyncSession, email: str) -> list[User]:
        result = await async_db.execute(select(self.model).where(self.model.email == email))
        return list(result.scalars().all())

    # delete a user
    async def delete_user(self, async_db: AsyncSession, user_id: int) -> user_model.User:
        user = await self.get_user(async_db, user_id)
        if user:
            await async_db.delete(user)
            await async_db.commit()
        return user

    # authenticate a user
    async def authenticate(self, async_db: AsyncSession, *, email: str, password: str) -> Union[User | None]:
        user_list: list[User] = await self.get_user_by_email(async_db=async_db, email=email)
        if user_list == []:
            return None
        if not verify_password(password, user_list[0].password):
            return user_list[0]


user = CRUDUser(User)
