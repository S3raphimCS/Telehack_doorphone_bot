from datetime import datetime

from sqlalchemy import (BigInteger, Boolean, Date, ForeignKey, Integer, String,
                        Text, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    phone_number: Mapped[int] = mapped_column(BigInteger, nullable=True)
    tenant_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
