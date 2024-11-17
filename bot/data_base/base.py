from .database import Base, async_session, engine
from sqlalchemy.orm import class_mapper


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def to_dict(self) -> dict:
    """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
    # Получаем маппер для текущей модели
    columns = class_mapper(self.__class__).columns
    # Возвращаем словарь всех колонок и их значений
    return {column.key: getattr(self, column.key) for column in columns}