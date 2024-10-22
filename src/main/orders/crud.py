from typing import Any, Union, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select
from .model import Order

import model as order_model, schema as order_schema
from src.main.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDOrder(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def create_order(
        self, db: AsyncSession, *, obj_in: Union[order_schema.OrderCreate, dict[str, Any]]
    ) -> order_model.Order:
        if isinstance(obj_in, dict):
            order_data = obj_in
        else:
            order_data = obj_in.model_dump(exclude_unset=True)

        db_order = self.model(**order_data)
        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)
        return db_order

    async def get_order(self, db: AsyncSession, order_id: int) -> order_model.Order | None:
        result = await db.execute(select(self.model).where(self.model.id == order_id))
        return result.scalars().first()

    async def get_orders(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[order_model.Order]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def update_order(
        self, db: AsyncSession, *, db_obj: order_model.Order, obj_in: Union[order_schema.OrderUpdate, dict[str, Any]]
    ) -> order_model.Order:
        """
        Update order in the database. Only provided fields will be updated.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete_order(self, db: AsyncSession, order_id: int) -> order_model.Order:
        order = await self.get_order(db, order_id)
        if order:
            await db.delete(order)
            await db.commit()
        return order


order = CRUDOrder(Order)