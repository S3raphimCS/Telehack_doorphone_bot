from typing import List, Optional, Tuple

from create_bot import logger
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from .base import connection, to_dict
from .models import User

from utils.http_queries import (
    get_tenants_apartments,
    get_user_tenant_id,
    get_tenants_doorphones,
    get_image_from_doorphone
)

from sqlalchemy.ext.asyncio import AsyncSession


@connection
async def set_user(session: AsyncSession, tg_id: int) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id, )
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as err:
        logger.error(f"Ошибка при добавлении пользователя: {err}")
        await session.rollback()


@connection
async def check_tenant(session: AsyncSession, phone_number: int) -> bool:
    user = await session.scalar(select(User).filter_by(phone_number=phone_number))
    tenant_id = get_user_tenant_id(user.phone_number)
    if tenant_id:
        try:
            user.tenant_id = tenant_id
            await session.commit()
            return True
        except SQLAlchemyError as err:
            logger.error(f"Ошибка при проверке или добавлении tenant_id пользователя: {err}")
            await session.rollback()
            return False
    else:
        return False


@connection
async def add_number_to_user(session: AsyncSession, tg_id: int, phone_number: int) -> None:
    try:
        await session.execute(update(User).where(User.id == tg_id).values(phone_number=phone_number))
        await session.commit()
        return
    except SQLAlchemyError as err:
        logger.error(f"Ошибка при добавлении номера телефона пользователя: {err}")
        await session.rollback()


@connection
async def get_tenant_id(session: AsyncSession, tg_id: int) -> int | None:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))
        tenant_id = user.tenant_id
        return tenant_id
        # user = to_dict(user)
        # if user:
        #     return user
        # else:
        #     return None
    except SQLAlchemyError as err:
        logger.error(f"Ошибка при получении tenant_id пользователя: {err}")
