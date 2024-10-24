from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

from . import crud as customer_crud, schema as customer_schema
from ..auth import model, dependencies
from ..core.dependencies import get_session

router = APIRouter()


# route to create a customer
@router.post("/customer", response_model=customer_schema.Customer)
async def create_customer(
    customer: customer_schema.CustomerCreate,
    async_db: AsyncSession = Depends(get_session),
    current_user: model.User = Depends(dependencies.get_current_user)
):
    async with async_db as session:

        if not current_user.email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to create an order"
            )
        created_customer = await customer_crud.customer.create_customer(async_db=session, obj_in=customer)
    return created_customer


# Gwt customer by ID
@router.get("/customer/{customer_id}", response_model=customer_schema.Customer)
async def get_customer_by_id(
    customer_id: int,
    async_db: AsyncSession = Depends(get_session)
):
    async with async_db as session:
        customer = await customer_crud.customer.get_customer(async_db=session, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# Filter customer by country
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
    async with async_db as session:
        customers = await customer_crud.customer.get_customers(
            async_db=session,
            skip=skip,
            limit=limit,
            country=country,
            sort_by=sort_by,
            order=order,
            use_cache=use_cache
        )
    return customers


#update customer by ID
@router.put("/customers/{customer_id}", response_model=customer_schema.Customer)
async def update_customer(
        customer_id: int,
        customer_in: customer_schema.CustomerUpdate,
        async_db: AsyncSession = Depends(get_session)
):
    async with async_db as session:
        db_customer = await customer_crud.customer.get_customer(async_db=session, customer_id=customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        updated_customer = await customer_crud.customer.update_customer(async_db=session, db_obj=db_customer,
                                                                        obj_in=customer_in)
        return updated_customer


# Delete customer
@router.delete("/customer/{customer_id}", response_model=customer_schema.Customer)
async def delete_customer(
        customer_id: int,
        async_db: AsyncSession = Depends(get_session)
):
    async with async_db as session:
        customer = await customer_crud.customer.get_customer(async_db=session, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    deleted_customer = await customer_crud.customer.delete_customer(async_db=async_db, customer_id=customer_id)
    return deleted_customer