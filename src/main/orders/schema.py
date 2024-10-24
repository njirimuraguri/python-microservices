from pydantic import BaseModel, ConfigDict
from datetime import datetime


# shared properties
class OrderBase(BaseModel):
    item: str
    amount: int
    time: datetime
    phone_number: str


# Properties to receive on order creation
class OrderCreate(OrderBase):
    customer_id: int


# Properties to receive via API on order update
class OrderUpdate(OrderBase):
        pass


# Properties shared by models stored in DB
class OrderInDBBase(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# Properties to return to client
class Order(OrderInDBBase):
    pass


# properties stored in DB
class OrderInDB(OrderInDBBase):
    pass