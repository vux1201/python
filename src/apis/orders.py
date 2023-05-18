import random
import string

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apis.deps import get_db, get_current_user, get_current_admin
from models.order import Order, OrderItem
from models.user import User
import schemas
import crud


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get(
    "/me", response_model=list[schemas.Order], description="Lấy tất cả order của user"
)
async def read_orders_me(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    orders = current_user.orders
    return orders


@router.get(
    "/",
    response_model=list[schemas.OrderAdmin],
    dependencies=[Depends(get_current_admin)],
    description="Admin lấy tất cả order",
)
async def read_orders(
    *,
    db: Session = Depends(get_db),
    skip: int = 1,
    limit: int = 10,
):
    orders = crud.order.get_multi(db=db, skip=skip, limit=limit)
    return orders


@router.post(
    "/me",
    response_model=schemas.Order,
    description="User sau khi đăng nhập tạo order mới",
)
async def create_order(
    *,
    db: Session = Depends(get_db),
    order_items_in: list[schemas.OrderItemCreate],
    current_user: User = Depends(get_current_user),
):
    """
    Cần truyền lên list các mẫu sản phẩm, mỗi mẫu gồm các thông tin như trong Example:
        - product_variant_id: id của mẫu sp
        - qty: số lượng mua mẫu này
        - price: giá trị tổng của mẫu này (qty * product_variant.price)
    """
    code = "".join(
        random.choices(string.digits, k=6) +
        random.choices(string.ascii_uppercase, k=8)
    )
    order = Order(code=code, status=0, user_id=current_user.id, total=0)
    total_price = 0
    for item in order_items_in:
        total_price += item.price
        order_item = OrderItem(
            product_variant_id=item.product_variant_id, qty=item.qty)
        order.order_items.append(order_item)
    setattr(order, "total", total_price)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get(
    "/{order_id}",
    response_model=schemas.Order,
    dependencies=[Depends(get_current_user)],
    description="Xem chi tiết order",
)
async def read_order(*, db: Session = Depends(get_db), order_id: int):
    """
    Lấy thông tin order theo id
    """
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found"
        )
    return order


@router.put(
    "/{order_id}",
    response_model=schemas.Order,
    dependencies=[Depends(get_current_admin)],
    description="Sửa order (chỉ admin, chỉ để sửa trạng thái order)",
)
async def update_order(
    *, db: Session = Depends(get_db), order_id: int, order_in: schemas.OrderUpdate
):
    """
    Sửa order theo id.
    Chỉ admin sửa, ở đây chỉ đang hỗ trợ sửa trạng thái order:
        - 0 (mặc định khi tạo order thì status = 0): đặt thành công
        - 1: đang chuẩn bị hàng
        - 2: đang giao hàng
        - 3: đã giao hàng
    """
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found"
        )
    order = crud.order.update(db=db, db_obj=order, obj_in=order_in)
    return order
