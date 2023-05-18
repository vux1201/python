from typing import Any

import jwt
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_db
from core.security import verify_password
from models.user import User
from utils import create_access_token, password_strong

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
async def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Login API"""
    stmt = select(User).where(User.email == form_data.username)
    user = db.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không tồn tại user với email này",
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authenticate failed",
        )
    return {"access_token": create_access_token(user.email), "token_type": "bearer"}


@router.post("/register", response_model=schemas.User)
async def register(
    db: Session = Depends(get_db),
    *,
    firstname: str = Body(...),
    lastname: str = Body(...),
    email: EmailStr = Body(...),
    password: str = Body(...),
    phone_number: str = Body(...),
    address: str = Body(...)
) -> Any:
    """Register API"""
    stmt = select(User).where(User.email == email)
    user = db.scalar(stmt)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    if not password_strong(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu phải có ít nhất 8 kí tự, bao gồm 1 chữ hoa, 1 chữ thường, 1 chữ số, 1 kí tự đặc biệt",
        )
    user_in = schemas.UserCreate(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone_number=phone_number,
        address=address,
        password=password,
        is_admin=False,
        is_staff=False,
    )
    user = crud.user.create(db=db, obj_in=user_in)
    return user
