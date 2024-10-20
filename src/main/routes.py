from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .customer import model as customer_model, schema as customer_schema, crud as crud_customer
from ..main.orders import model as order_model, schema as order_schema

from ..main.core.dependencies import get_session

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to the FastAPI Main Service"}


@router.post("/customers", response_model=customer_schema.Customer)
async def create_customer(customer: customer_schema.CustomerCreate, async_db: AsyncSession = Depends(get_session)):
    customer = await crud_customer.customer.create_customer(async_db=async_db, obj_in=customer)
    return customer
