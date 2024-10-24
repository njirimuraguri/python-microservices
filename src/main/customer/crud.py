import json

from typing import Any, Union, Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select

from src.main.customer import model as customer_model
from src.main.customer import schema as customer_schema
from ..database.base import Base
from .model import Customer

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDCustomer(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    # create customer
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

    # function to get a customer
    async def get_customer(self, async_db: AsyncSession, customer_id: int) -> customer_model.Customer | None:
        result = await async_db.execute(select(self.model).where(self.model.id == customer_id))
        return result.scalars().first()

    redis_client = redis.Redis.from_url("redis://localhost")

    # Sorting, Pagination  and Filtering
    async def get_customers(
            self,
            async_db: AsyncSession,
            skip: int = 0,
            limit: int = 100,
            country: str = None,  # For filtering by country
            sort_by: str = "name",  # Sorting field
            order: str = "asc",  # Sorting direction
            use_cache: bool = True,  # Caching control
            cache_key: str = "customers"
    ) -> list[customer_model.Customer]:

        # Check cache first
        if use_cache:
            cached_data = await redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

        # Build the query
        query = select(self.model)

        # Apply filtering
        if country:
            query = query.where(self.model.country == country)

        # Apply sorting
        if order == "desc":
            query = query.order_by(getattr(self.model, sort_by).desc())
        else:
            query = query.order_by(getattr(self.model, sort_by).asc())

        # Pagination
        query = query.offset(skip).limit(limit)

        result = await async_db.execute(query)
        customers = list(result.scalars().all())

        # Cache the result
        if use_cache:
            await redis.set(cache_key, json.dumps([jsonable_encoder(customer) for customer in customers]), ex=60)

        return customers

    # function to update a customer according to ID
    async def update_customer(
            self, async_db: AsyncSession, *, db_obj: customer_model.Customer,
            obj_in: Union[customer_schema.CustomerUpdate, dict[str, Any]]
    ) -> customer_model.Customer:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        async_db.add(db_obj)
        await async_db.commit()
        await async_db.refresh(db_obj)
        return db_obj

    # Delete Customer
    async def delete_customer(self, async_db: AsyncSession, customer_id: int) -> customer_model.Customer:
        customer = await self.get_customer(async_db, customer_id)
        if customer:
            await async_db.delete(customer)
            await async_db.commit()
        return customer


customer = CRUDCustomer(Customer)
