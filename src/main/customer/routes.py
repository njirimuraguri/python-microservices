from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from . import crud as customer_crud, schema as customer_schema
from ..core.dependencies import get_session

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to the FastAPI Main Service"}


@router.post("/customers", response_model=customer_schema.Customer)
async def create_customer(customer: customer_schema.CustomerCreate, async_db: AsyncSession = Depends(get_session)):
    customer = await customer_crud.customer.create_customer(async_db=async_db, obj_in=customer)
    return customer
