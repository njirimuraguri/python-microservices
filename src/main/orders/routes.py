from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from . import crud as order_crud, schema as order_schema
from ..core.dependencies import get_session

router = APIRouter()


@router.post("/orders", response_model=order_schema.Order)
async def create_customer(order: order_schema.OrderCreate, async_db: AsyncSession = Depends(get_session)):
    order = await order_crud.order.create_order(async_db=async_db, obj_in=order)
    return order
