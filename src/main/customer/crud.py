from typing import Any, Union, Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select

import model as customer_model, schema as customer_schema
from .model import Customer
from ..database.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDCustomer(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def create_customer(
        self, async_db: AsyncSession, *, obj_in: Union[customer_schema.CustomerCreate, dict[str, Any]]
    ) -> customer_model.Customer:
        if isinstance(obj_in, dict):
            customer_data = obj_in
        else:
            customer_data = obj_in.model_dump(exclude_unset=True)

        db_customer = self.model(**customer_data)
        async_db.add(db_customer)
        await async_db.commit()
        await async_db.refresh(db_customer)
        return db_customer

    async def get_customer(self, async_db: AsyncSession, customer_id: int) -> customer_model.Customer | None:
        result = await async_db.execute(select(self.model).where(self.model.id == customer_id))
        return result.scalars().first()

    async def get_customers(self, async_db: AsyncSession, skip: int = 0, limit: int = 100) -> list[customer_model.Customer]:
        result = await async_db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_customer(
        self, async_db: AsyncSession, *, db_obj: customer_model.Customer, obj_in: Union[customer_schema.CustomerUpdate, dict[str, Any]]
    ) -> customer_model.Customer:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        async_db.add(db_obj)
        await async_db.commit()
        await async_db.refresh(db_obj)
        return db_obj

    async def delete_customer(self, async_db: AsyncSession, customer_id: int) -> customer_model.Customer:
        customer = await self.get_customer(async_db, customer_id)
        if customer:
            await db.delete(customer)
            await db.commit()
        return customer


customer = CRUDCustomer(Customer)
