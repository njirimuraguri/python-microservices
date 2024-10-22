from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
# from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column, as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    created_by: Mapped[int] = mapped_column(
        nullable=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, # , server_default=func.now(), server_onupdate=FetchedValue()
    )
    updated_by: Mapped[int] = mapped_column(
        nullable=True,
    )
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()