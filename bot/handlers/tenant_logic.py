import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from data_base.queries import get_tenant_id
from keyboards.all_kb import main_menu_keyboard, remove_state_kb
from utils.http_queries import (get_image_from_doorphone,
                                get_tenants_apartments, get_tenants_doorphones,
                                open_door)

router = Router()


def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None


class Doorphone_Form(StatesGroup):
    address = State()
    doorphone = State()


class CameraForm(StatesGroup):
    address = State()
    doorphone = State()


async def get_doorphones_by_tenant_id(message: Message):
    tenant_id = await get_tenant_id(message.from_user.id)
    tenants_apartments = get_tenants_apartments(tenant_id)
    doorphones = []
    for apartment in tenants_apartments:
        doorphones.append(get_tenants_doorphones(apartment[0], tenant_id))
    return tenants_apartments, doorphones


@router.message(F.text == '📋Список доступных домофонов')
async def doorphones_list(message: Message):
    tenant_id = await get_tenant_id(message.from_user.id)
    answer = "У вас нет прав на получение данной информации"
    if tenant_id:
        answer = 'Список доступных домофонов по адресам:'
        tenants_apartments, doorphones = await get_doorphones_by_tenant_id(message)
        counter = 0
        for i in range(len(doorphones)):
            answer += '\n\n'
            answer += f"{tenants_apartments[i][1]}:\n"
            for j in range(len(doorphones[i])):
                counter += 1
                answer += f'{counter}) {doorphones[i][j][1]}\n'
    await message.answer(text=f"{answer}")


@router.message(F.text == '🔓Открыть домофон')
async def start_open_doorphones_questionary(message: Message, state: FSMContext):
    tenant_id = await get_tenant_id(message.from_user.id)
    if tenant_id:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            tenants_apartments, doorphones = await get_doorphones_by_tenant_id(message)
            answer = "Выберите адрес:\n"
            for i in range(len(tenants_apartments)):
                answer += f"{i + 1}){tenants_apartments[i][1]}\n"
            await message.answer(text=answer, reply_markup=remove_state_kb())
        await state.set_state(Doorphone_Form.address)
    else:
        await message.answer(text="Вы не являетесь жильцом")


@router.message(F.text, Doorphone_Form.address)
async def doorphone_form_capture_address(message: Message, state: FSMContext):
    tenants_apartments, doorphones = await get_doorphones_by_tenant_id(message)
    tenant_id = await get_tenant_id(message.from_user.id)
    number = extract_number(message.text)

    if not number or number > len(tenants_apartments):
        await message.reply("Введено некорректное значение")
        return

    await state.update_data(address=tenants_apartments[number - 1][0])
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        actual_doorphones = get_tenants_doorphones(tenants_apartments[number - 1][0], tenant_id)
        answer = "Выберите домофон для открытия:\n"
        for i in range(len(actual_doorphones)):
            answer += f'{i + 1}) {actual_doorphones[i][1]}\n'
    await message.answer(text=answer, reply_markup=remove_state_kb())
    await state.set_state(Doorphone_Form.doorphone)


@router.message(F.text, Doorphone_Form.doorphone)
async def doorphone_form_capture_doorphone(message: Message, state: FSMContext):
    tenant_id = await get_tenant_id(message.from_user.id)
    number = extract_number(message.text)
    apartment = await state.get_data()
    apartment = apartment["address"]
    actual_doorphones = get_tenants_doorphones(apartment, tenant_id)

    if number > len(actual_doorphones) or not number:
        await message.reply("Введено некорректное значение")
        return
    await state.update_data(doorphone=actual_doorphones[number - 1][0])
    open_door_message = open_door(tenant_id, actual_doorphones[number - 1][0], 0)
    if open_door_message:
        await message.answer(
            text=f"Домофон «{actual_doorphones[number - 1][1]}» успешно открыт",
            reply_markup=main_menu_keyboard(message.from_user.id)
        )
    else:
        await message.answer(text="Ошибка при открытии домофона")
    await state.clear()


@router.message(F.text == '📸Снимки с домофонов')
async def start_get_camera_images_questionary(message: Message, state: FSMContext):
    tenant_id = await get_tenant_id(message.from_user.id)
    if tenant_id:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            tenants_apartments, doorphones = await get_doorphones_by_tenant_id(message)
            answer = "Выберите адрес:\n"
            for i in range(len(tenants_apartments)):
                answer += f"{i + 1}) {tenants_apartments[i][1]}\n"
            await message.answer(text=answer, reply_markup=remove_state_kb())
        await state.set_state(CameraForm.address)
    else:
        await message.answer(text="Вы не являетесь жильцом")


@router.message(F.text, CameraForm.address)
async def camera_form_capture_address(message: Message, state: FSMContext):
    tenants_apartments, doorphones = await get_doorphones_by_tenant_id(message)
    tenant_id = await get_tenant_id(message.from_user.id)
    number = extract_number(message.text)

    if not number or number > len(tenants_apartments):
        await message.reply("Введено некорректное значение")
        return

    await state.update_data(address=tenants_apartments[number - 1][0])
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        actual_doorphones = get_tenants_doorphones(tenants_apartments[number - 1][0], tenant_id)
        answer = "Выберите домофон для просмотра:\n"
        for i in range(len(actual_doorphones)):
            answer += f'{i + 1}) {actual_doorphones[i][1]}\n'
        await message.answer(text=answer, reply_markup=remove_state_kb())
    await state.set_state(CameraForm.doorphone)


@router.message(F.text, CameraForm.doorphone)
async def camera_form_capture_doorphone(message: Message, state: FSMContext):
    tenant_id = await get_tenant_id(message.from_user.id)
    number = extract_number(message.text)
    apartment = await state.get_data()
    apartment = apartment["address"]
    actual_doorphones = get_tenants_doorphones(apartment, tenant_id)

    if number > len(actual_doorphones) or not number:
        await message.reply("Введено некорректное значение")
        return
    doorphone_id = actual_doorphones[number - 1][0]
    await state.update_data(doorphone=doorphone_id)
    get_camera_image_url = get_image_from_doorphone(tenant_id, [doorphone_id], ["JPEG"])
    try:
        if get_camera_image_url:
            await message.answer_photo(
                photo=get_camera_image_url,
                reply_markup=main_menu_keyboard(message.from_user.id)
            )
        else:
            await message.answer(
                text="Ошибка при открытии домофона",
                reply_markup=main_menu_keyboard(message.from_user.id)
            )
    except Exception:
        await message.answer(
            text="Ошибка при получении изображения. Возможно, камера не работает",
            reply_markup=main_menu_keyboard(message.from_user.id)
        )
    await state.clear()


@router.callback_query(F.data == 'remove_state')
async def remove_state(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()


@router.callback_query(F.data.startswith("open_doorphone"))
async def open_doorphone_on_endpoint(call: CallbackQuery):
    _, domofon_id, tenant_id = call.data.split(":")
    result = open_door(tenant_id, domofon_id, 0)
    if result:
        await bot.send_message(call.from_user.id, "Домофон успешно открыт!",
                               reply_markup=main_menu_keyboard(call.from_user.id))
        await call.message.edit_reply_markup(reply_markup=None)
    else:
        await bot.send_message(call.from_user.id, "Ошибка при открытии домофона")


@router.message()
async def wrong_command(message: Message):
    await message.answer(text="Введена неправильная команда", reply_markup=main_menu_keyboard(message.from_user.id))
