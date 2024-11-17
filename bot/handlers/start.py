from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from data_base.queries import set_user
from keyboards.all_kb import contact_keyboard


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await set_user(tg_id=message.from_user.id)

    await message.answer(
        "Привет, Я бот для управления домофоном.\n"
        "Для продолжения работы вам необходимо предоставить информацию о вашем номере телефона.",
        reply_markup=contact_keyboard(message.from_user.id))
