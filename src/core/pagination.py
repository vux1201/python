from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy import select, func
from sqlalchemy.orm import Session


class PageParams(BaseModel):
    """Request query params for paginated API."""

    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)


T = TypeVar("T", bound=BaseModel)


class PagedResponseSchema(GenericModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: List[T]


def paginate(
    db: Session, query, page_params: PageParams, ResponseSchema: T
) -> PagedResponseSchema[T]:
    """Paginate the query."""

    paginated_query = (
        db.scalars(
            query.offset((page_params.page - 1) * page_params.size).limit(
                page_params.size
            )
        )
        .unique()
        .all()
    )

    return PagedResponseSchema(
        total=db.scalar(select(func.count()).select_from(query)),
        page=page_params.page,
        size=page_params.size,
        results=[ResponseSchema.from_orm(item) for item in paginated_query],
    )
