from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from decouple import config

engine = create_async_engine(
    url=f"postgresql+asyncpg://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}/{config('POSTGRES_DB')}")
async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
