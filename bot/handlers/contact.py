from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from create_bot import admins, bot

from keyboards.all_kb import start_kb, contact_keyboard, main_menu_keyboard
from sqlalchemy.exc import SQLAlchemyError

from data_base.queries import check_tenant, add_number_to_user

router = Router()


@router.message(F.contact)
async def get_contact(message: Message):
    contact = message.contact
    phone_number = int(contact.phone_number[1:])
    await add_number_to_user(message.from_user.id, phone_number)
    is_tenant = await check_tenant(phone_number)
    await message.answer(f"Спасибо, {contact.first_name}.\n"
                         f"Ваш номер {contact.phone_number} был получен",
                         reply_markup=ReplyKeyboardRemove())
    if is_tenant:
        await message.answer(
            f"Авторизация в боте прошла успешно\n"
            f"Теперь вы можете управлять вашими домофонами",
            reply_markup=main_menu_keyboard(message.from_user.id)
        )
    else:
        await message.answer(
            text="Вы не являетесь пользователем Инсис",
            reply_markup=ReplyKeyboardRemove()
        )
