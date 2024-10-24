from datetime import datetime
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, mapped_column, Mapped

from ..database.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    item: Mapped[str] = mapped_column(index=True, nullable=True)
    amount: Mapped[int] = mapped_column(index=True, nullable=True)
    time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), index=True, nullable=True)
    phone_number: Mapped[int] = mapped_column(index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)

    customer = relationship("Customer", back_populates="orders") #  relationship between customer and order table

