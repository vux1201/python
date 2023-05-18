import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import settings
from db.session import DBSession
from models.user import User

oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")


async def get_db():
    db: Session = DBSession
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth_schema)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, ["HS256"])
    except:
        raise credentials_exception
    username = payload.get("sub")
    if not username:
        raise credentials_exception
    stmt = select(User).where(User.email == username)
    user = db.scalar(stmt)
    if not user:
        raise credentials_exception
    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not admin",
        )
    return current_user
