from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import emoji

# Главное меню пользователя
main_menu = [
    [InlineKeyboardButton(text="Список задач", callback_data="my_tasks")],
    [InlineKeyboardButton(text="Новая задача", callback_data="new_task")],
    [InlineKeyboardButton(text="Редактировать профиль", callback_data="change_profile")]
]
main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu)


# Меню создания новой задачи
new_tasks_menu = [
    [InlineKeyboardButton(text="Название задачи", callback_data="task_name")],
    [InlineKeyboardButton(text="Описание задачи", callback_data="task")],
    [InlineKeyboardButton(text="Взаимосвязи", callback_data="relationship")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
]
new_tasks_menu = InlineKeyboardMarkup(inline_keyboard = new_tasks_menu)


# Меню удаления задач


# Меню редактирования задач


# Меню статуса задачи
tasks_status_menu = [
    [InlineKeyboardButton(text="Готово", callback_data="task_name")],
    [InlineKeyboardButton(text="Удалить", callback_data="del")],
    [InlineKeyboardButton(text="Редактировать", callback_data="edit")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
]
tasks_status_menu = InlineKeyboardMarkup(inline_keyboard = tasks_status_menu)