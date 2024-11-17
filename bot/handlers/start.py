from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from create_bot import admins, bot

from keyboards.all_kb import start_kb, contact_keyboard
from sqlalchemy.exc import SQLAlchemyError

from data_base.queries import set_user
from data_base.queries import check_tenant

from middlewares.throttle import ThrottlingMiddleware


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await set_user(tg_id=message.from_user.id)

    await message.answer(
        "Привет, Я бот для управления домофоном.\n"
        "Для продолжения работы вам необходимо предоставить информацию о вашем номере телефона.",
        reply_markup=contact_keyboard(message.from_user.id))
