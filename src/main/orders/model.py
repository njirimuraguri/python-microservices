from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    amount = Column(Integer, index=True)
    time = Column(DateTime, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)

    customer = relationship("Customer", back_populates="orders")
