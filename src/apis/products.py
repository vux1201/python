from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_admin, get_db
from core.pagination import PagedResponseSchema, PageParams, paginate

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "/",
    response_model=PagedResponseSchema[schemas.Product],
    summary="Lấy danh sách sản phẩm",
)
async def read_products(
    *,
    db: Session = Depends(get_db),
    category_id: list[int] | None = Query(default=None),
    brand_id: list[int] | None = Query(default=None),
    keyword: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    page_params: PageParams = Depends(),
):
    """
    Các tham số: truyền tham số dạng ?skip=0&limit=10...
    - Phân trang:
        - skip: để phân trang, vd trang 1 thì skip = 0, trang 2 thì skip = 1 * limit
        - limit: số sản phẩm trong 1 trang
    - Tìm kiếm:
        - keyword: để tìm kiếm theo tên sản phẩm
        - category_id: truyền id của danh mục sản phẩm
        - brand_id: id của thương hiệu
    """
    query = crud.product.get_multi_filter(
        category_id=category_id,
        brand_id=brand_id,
        keyword=keyword,
        min_price=min_price,
        max_price=max_price,
    )
    return paginate(db, query, page_params, schemas.Product)


@router.post(
    "/",
    response_model=schemas.Product,
    dependencies=[Depends(get_current_admin)],
    summary="Tạo sản phẩm mới (chỉ admin)",
)
async def create_product(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.ProductCreate,
):
    item = crud.product.create(db=db, obj_in=obj_in)
    return item


@router.get(
    "/{id}",
    response_model=schemas.Product,
    summary="Xem sản phẩm",
)
async def read_product(*, db: Session = Depends(get_db), id: int):
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Khong ton tai san pham nay"
        )
    return product


@router.put(
    "/{id}",
    response_model=schemas.Product,
    dependencies=[Depends(get_current_admin)],
    summary="Sửa sản phẩm (chỉ admin)",
)
async def update_product(
    *, db: Session = Depends(get_db), id: int, product_in: schemas.ProductUpdate
):
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product


@router.delete(
    "/{id}",
    response_model=schemas.Product,
    dependencies=[Depends(get_current_admin)],
    summary="Xóa sản phẩm (chỉ admin)",
)
async def delete_product(*, db: Session = Depends(get_db), id: int):
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    product = crud.product.remove(db=db, db_obj=product)
    return product
