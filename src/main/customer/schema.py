from typing import Union
from pydantic import BaseModel, EmailStr, ConfigDict


# Shared properties
class CustomerBase(BaseModel):
    name: Union[str, None]
    email: EmailStr
    code: Union[str, None]
    country: Union[str, None]
    phone_number: Union[str, None]
    gender: Union[str, None]


# Properties to receive on customer creation
class CustomerCreate(CustomerBase):
    password: str


# Properties to receive via API on update by customer
class CustomerUpdate(CustomerBase):
    pass


# Properties shared by models stored in DB
class CustomerInDBBase(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# Properties to return to client
class Customer(CustomerInDBBase):
    pass


# properties stored in DB
class CustomerInDB(CustomerInDBBase):
    pass