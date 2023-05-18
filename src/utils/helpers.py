from datetime import datetime, timedelta
from functools import reduce
from typing import Any

import jwt

from core.config import settings


def create_access_token(subject: str | Any):
    # expire = datetime.utcnow() + timedelta(minutes=15)
    # to_encode = {"exp": expire, "sub": str(subject)}
    to_encode = {"sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY)
    return encoded_jwt


def to_snake_case(text: str) -> str:
    return reduce(lambda x, y: x + ("_" if y.isupper() else "") + y, text).lower()
