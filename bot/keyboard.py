from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


kb = InlineKeyboardBuilder()
kb.add(
    types.InlineKeyboardButton(text="Получить данные по товару", callback_data="callback_data")
)

