from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

from . import crud as customer_crud, schema as customer_schema
from ..core.dependencies import get_session

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to the FastAPI Main Service"}


@router.post("/customer", response_model=customer_schema.Customer)
async def create_customer(
    customer: customer_schema.CustomerCreate,
    async_db: AsyncSession = Depends(get_session)
):
    created_customer = await customer_crud.customer.create_customer(async_db=async_db, obj_in=customer)
    return created_customer


@router.get("/customer/{customer_id}", response_model=customer_schema.Customer)
async def get_customer_by_id(
    customer_id: int,
    async_db: AsyncSession = Depends(get_session)
):
    customer = await customer_crud.customer.get_customer(async_db=async_db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/customer", response_model=List[customer_schema.Customer])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    country: str = None,
    sort_by: str = "name",
    order: str = "asc",
    use_cache: bool = True,
    async_db: AsyncSession = Depends(get_session)
):
    customers = await customer_crud.customer.get_customers(
        async_db=async_db,
        skip=skip,
        limit=limit,
        country=country,
        sort_by=sort_by,
        order=order,
        use_cache=use_cache
    )
    return customers

@router.put("/customers/{customer_id}", response_model=customer_schema.Customer)
async def update_customer(
        customer_id: int,
        customer_in: customer_schema.CustomerUpdate,
        async_db: AsyncSession = Depends(get_session)
):
    db_customer = await customer_crud.customer.get_customer(async_db=async_db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    updated_customer = await customer_crud.customer.update_customer(async_db=async_db, db_obj=db_customer,
                                                                    obj_in=customer_in)
    return updated_customer



@router.delete("/customer/{customer_id}", response_model=customer_schema.Customer)
async def delete_customer(
        customer_id: int,
        async_db: AsyncSession = Depends(get_session)
):
    customer = await customer_crud.customer.get_customer(async_db=async_db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    deleted_customer = await customer_crud.customer.delete_customer(async_db=async_db, customer_id=customer_id)
    return deleted_customer