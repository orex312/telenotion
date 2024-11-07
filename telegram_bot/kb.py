from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="Start", callback_data="\start")],
    [InlineKeyboardButton(text="Добавить пользователя", callback_data="generate_text")],
    [InlineKeyboardButton(text="Список задач", callback_data="generate_text")],
    [InlineKeyboardButton(text="Новая задача", callback_data="generate_text")],
    [InlineKeyboardButton(text="Что-нибудь еще", callback_data="generate_text")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])