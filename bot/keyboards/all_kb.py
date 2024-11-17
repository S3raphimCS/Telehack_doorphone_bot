from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def start_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="")],
        [KeyboardButton(text="")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def contact_keyboard(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="📱 Отправить", request_contact=True)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard


def main_menu_keyboard(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text="📋Список доступных домофонов")],
        [KeyboardButton(text="🔓Открыть домофон"), KeyboardButton(text="📸Снимки с домофонов")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard


def remove_state_kb():
    kb_list = [
        [InlineKeyboardButton(text="⛔️Отменить", callback_data="remove_state")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def open_door_kb_with_tenant_id_and_domofon_id(data):
    kb_list = [
        [InlineKeyboardButton(text="🔓Открыть домофон", callback_data=f"open_doorphone:{data[0]}:{data[1]}")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
