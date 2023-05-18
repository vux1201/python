import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from utils import to_snake_case


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return to_snake_case(cls.__name__)

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True
    )
    deleted_at: Mapped[datetime.datetime] = mapped_column(nullable=True)
