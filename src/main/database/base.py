from sqlalchemy.ext.declarative import as_declarative, declared_attr
# Generate __tablename__ automatically
@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

