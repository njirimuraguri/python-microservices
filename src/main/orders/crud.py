import json

from datetime import datetime
from typing import Any, Union, Generic, Type, TypeVar
from django.core.cache.backends import redis
import redis.asyncio as redis
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from .model import Order
from . import model as order_model, schema as order_schema
from src.main.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDOrder(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    # Create order
    async def create_order(
        self, async_db: AsyncSession, *, obj_in: Union[order_schema.OrderCreate, dict[str, Any]]
    ) -> order_model.Order:
        if isinstance(obj_in, dict):
            order_data = obj_in
        else:
            order_data = obj_in.model_dump(exclude_unset=True)

        async with async_db as session:
            db_order = self.model(**order_data)
            session.add(db_order)
            await session.commit()
            await session.refresh(db_order)
            return db_order

    # get orders bt date range
    async def get_orders_by_date_range(
            async_db: AsyncSession, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100
    , self=None) -> list[order_model.Order]:
        query = select(self.model).where(self.model.time.between(start_date, end_date))
        query = query.offset(skip).limit(limit)
        result = await async_db.execute(query)
        return list(result.scalars().all())

    # get order by order id
    async def get_order(self, db: AsyncSession, order_id: int) -> order_model.Order | None:
        result = await db.execute(select(self.model).where(self.model.id == order_id))
        return result.scalars().first()

    redis_client = redis.Redis.from_url("redis://localhost")

    # Catching, Pagination and Sorting
    async def get_orders(
            async_db: AsyncSession,
            skip: int = 0,
            limit: int = 100,
            customer_id: int = None,
            item: str = None,
            sort_by: str = "time",
            order: str = "asc",
            use_cache: bool = True,
            cache_key: str = "orders"
    , self=None) -> list[order_model.Order]:

        # Check cache first
        if use_cache:
            cached_data = await redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

        # Start building the query
        query = select(self.model)

        # Apply filters if provided
        if customer_id:
            query = query.where(self.model.customer_id == customer_id)
        if item:
            query = query.where(self.model.item.ilike(f"%{item}%"))

        # Apply sorting
        if order == "desc":
            query = query.order_by(getattr(self.model, sort_by).desc())
        else:
            query = query.order_by(getattr(self.model, sort_by).asc())

        # Add pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        orders = list(result.scalars().all())

        # Cache the result if caching is enabled
        if use_cache:
            await redis.set(cache_key, json.dumps([jsonable_encoder(order) for order in orders]),
                            ex=60)  # Cache for 60 seconds

        return orders

    # update order
    async def update_order(
            self, db: AsyncSession, db_obj: order_model.Order, obj_in: Union[order_schema.OrderUpdate, dict[str, Any]]
    ) -> order_model.Order:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # delete oder by id
    async def delete_order(self, db: AsyncSession, order_id: int) -> order_model.Order:
        order = await self.get_order(db, order_id)
        if order:
            await db.delete(order)
            await db.commit()
        return order


order = CRUDOrder(Order)