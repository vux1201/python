from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.config import settings

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize properly relationships
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from db import base

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
DBSession = Session(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)
