from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const  # Здесь будем импортировать нужные виджеты
from environs import Env
from aiogram.filters import Command
from aiogram import Bot, types, F, Router
from aiogram.fsm.storage.memory import MemoryStorage # -- хранилища данных для состояний пользователей
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Select, Group, ScrollingGroup, SwitchTo
from magic_filter import F
import os
import sys


sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))

from tasks_operations import getTasksByUser, getTasksById, delTask, updateTaskDate, updateTaskStatus # type: ignore
from user_operations import addNewUser, getUserByLogin, getUserIdByName, getUserById # type: ignore 

env = Env()
env.read_env()

BOT_TOKEN = '7744140930:AAEtaKzDfFEls5-dc6KPMNui7Mzfv0zasiM'

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


class StartSG(StatesGroup):
    start = State()
    task_list = State()
    show_task = State()

# Это геттер
async def get_name(event_from_user: User, **kwargs):
    
    return {'user_name': event_from_user.first_name}

async def get_task_list(event_from_user: User, **kwargs):
    #await callback.message.answer(item_id)
    user_id = getUserByLogin(str(event_from_user.id))[0]["user_id"]
    resp = getTasksByUser(user_id)
    titles = []
    for i in resp:
        titles.append([i["title"],i["task_id"]])
    return {'tasks': resp, "titles": titles}

async def get_task(dialog_manager: DialogManager, **kwargs):
    #await callback.message.answer(item_id)
    task_id = dialog_manager.dialog_data["task_id"]
    #print(kwargs)
    resp = getTasksById(task_id)[0]
    return {'task': resp["task_id"], "title": resp["title"], "description": resp["description"]}

async def delete_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    #await callback.message.answer(item_id)
    task_id = dialog_manager.dialog_data["task_id"]
    #print(kwargs)
    delTask(task_id)
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, task_id: int):
    dialog_manager.dialog_data["task_id"] = task_id
    await dialog_manager.next()

async def go_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

start_dialog = Dialog(
    Window(
        Format(text="Привет {user_name}"),
        Group(
            SwitchTo(Const("Список задач"), id='task_list', state=StartSG.task_list),
            Button(Const("Создать задачу"), id="crawl"),
        ),
        state=StartSG.start,
        getter=get_name
    ),
    Window(
        Const(text="Список задач"),
        ScrollingGroup(
            Select(
                text=Format("{item[0]}"),
                id="time_select",
                items='titles',  # Список задач
                item_id_getter=lambda x: x[1],  # ID кнопки = текст кнопки
                on_click=go_next  # Обработчик выбора
            ),
            id="task_lists",
            width=1,  # Количество кнопок в строке
            height=5,  # Количество строк
        ),
        Button(Const("Меню"), id="task", on_click=go_main_menu),
        state=StartSG.task_list,
        getter=get_task_list
    ),
    Window(
        Format(text="{title}"),
        Format(text="{description}", when="description"),
        Group(
            Button(Const("Удалить"), id="task", on_click=delete_task),
            SwitchTo(Const("Назад"), id='task_list', state=StartSG.task_list),
            width=2,
        ),
        state=StartSG.show_task,
        getter=get_task
    )
)

router = Router()
# Этот классический хэндлер будет срабатывать на команду /start
@router.message(Command("start"))
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

if __name__ == "__main__":
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)
