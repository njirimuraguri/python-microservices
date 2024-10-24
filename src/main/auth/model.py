from sqlalchemy.orm import Mapped, mapped_column

from src.main.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)


