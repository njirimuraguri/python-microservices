from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from fastapi import HTTPException
from typing_extensions import List

from . import crud as order_crud, schema as order_schema
from ..core.dependencies import get_session

router = APIRouter()


@router.post("/orders", response_model=order_schema.Order)
async def create_order(order: order_schema.OrderCreate, async_db: AsyncSession = Depends(get_session)):
    order = await order_crud.order.create_order(async_db=async_db, obj_in=order)
    return order

@router.get("/orders/search", response_model=List[order_schema.Order])
async def get_orders_by_date_range(
    start_date: datetime,
    end_date: datetime,
    skip: int = 0,
    limit: int = 100,
    async_db: AsyncSession = Depends(get_session)
):
    orders = await order_crud.order.get_orders_by_date_range(
        db=async_db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
    )
    return orders


@router.get("/orders/{order_id}", response_model=order_schema.Order)
async def get_order_by_id(
    order_id: int,
    async_db: AsyncSession = Depends(get_session)
):
    order = await order_crud.order.get_order(async_db=async_db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/orders", response_model=List[order_schema.Order])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    item: str = None,
    sort_by: str = "time",
    order: str = "asc",
    use_cache: bool = True,
    async_db: AsyncSession = Depends(get_session)
):
    orders = await order_crud.order.get_orders(
        db=async_db,
        skip=skip,
        limit=limit,
        customer_id=customer_id,
        item=item,
        sort_by=sort_by,
        order=order,
        use_cache=use_cache
    )
    return orders


@router.put("/orders/{order_id}", response_model=order_schema.Order)
async def update_order(
        order_id: int,
        order_in: order_schema.OrderUpdate,
        async_db: AsyncSession = Depends(get_session)
):
    db_order = await order_crud.order.get_order(async_db=async_db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await order_crud.order.update_order(async_db=async_db, db_obj=db_order, obj_in=order_in)
    return updated_order


@router.delete("/orders/{order_id}", response_model=order_schema.Order)
async def delete_order(
        order_id: int,
        async_db: AsyncSession = Depends(get_session)
):
    order = await order_crud.order.get_order(async_db=async_db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    deleted_order = await order_crud.order.delete_order(async_db=async_db, order_id=order_id)
    return deleted_order
