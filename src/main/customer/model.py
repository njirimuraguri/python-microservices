from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, nullable=True)
    code: Mapped[str] = mapped_column(index=True, nullable=True)
    country: Mapped[str] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    gender: Mapped[str] = mapped_column(index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String)

    orders = relationship("Order", back_populates="customer")