from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_user, get_db, get_current_admin
from models.user import User
from utils.constants import GENDER_CHOICES
from utils.validate import password_strong
from core.pagination import PagedResponseSchema, PageParams, paginate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    tags=["users"],
    summary="Lấy thông tin user đang đăng nhập",
    response_model=schemas.User,
)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", tags=["users"], response_model=schemas.User)
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    firstname: str = Body(None),
    lastname: str = Body(None),
    email: EmailStr = Body(None),
    phone_number: str = Body(None),
    address: str = Body(None),
    gender: int = Body(None),
    password: str = Body(None),
):
    user = crud.user.get_by_email(db, email=email)
    if user and user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    if password and not password_strong(password):
        raise HTTPException(
            status_code=400,
            detail="Mật khẩu phải có ít nhất 8 kí tự, bao gồm 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 kí tự đặc biệt",
        )
    if gender and gender not in GENDER_CHOICES:
        raise HTTPException(
            status_code=400,
            detail="Giới tính gửi lên phải là 0 (Không biết), 1 (Nam), 2 (Nữ), 9 (Không cung cấp)",
        )
    user_in = schemas.UserUpdate(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone_number=phone_number,
        address=address,
        gender=gender,
        password=password,
    )
    user = crud.user.update(db=db, db_obj=current_user, obj_in=user_in)
    return user


@router.get(
    "/",
    tags=["users"],
    response_model=PagedResponseSchema[schemas.User],
    dependencies=[Depends(get_current_admin)],
    summary="Lấy danh sách user (admin)",
)
async def read_users(
    *,
    db: Session = Depends(get_db),
    keyword: str | None = None,
    page_params: PageParams = Depends(),
):
    query = crud.user.get_multi_filter(keyword=keyword)
    return paginate(db, query, page_params, schemas.User)


@router.get(
    "/{user_id}",
    tags=["users"],
    response_model=schemas.User,
    dependencies=[Depends(get_current_admin)],
    summary="Xem chi tiết user (admin)",
)
async def read_user(*, db: Session = Depends(get_db), user_id: int):
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Khong ton tai user nay"
        )
    return user
