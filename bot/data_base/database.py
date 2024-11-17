from datetime import datetime

from decouple import config
from sqlalchemy import func
from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    url="postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}".format(
        POSTGRES_USER=config('POSTGRES_USER'),
        POSTGRES_PASSWORD=config('POSTGRES_PASSWORD'),
        POSTGRES_HOST=config('POSTGRES_HOST'),
        POSTGRES_DB=config('POSTGRES_DB')
    )
)
async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
