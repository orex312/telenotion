from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from environs import Env
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage # -- хранилища данных для состояний пользователей
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Button, Select, Group, ScrollingGroup, SwitchTo, Cancel
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Calendar
from datetime import date, datetime
from magic_filter import F
from datetime import date
import os
import sys


sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))

from notion_operations import addNewNotion, delNotion, getActiveNotions # type: ignore
from tasks_operations import getTasksByUser, getTasksById, delTask, updateTaskDate, updateTaskStatus  # type: ignore
from tasks_operations import addNewTask, updateTaskTitle, updateTaskDescription  # type: ignore
from user_operations import addNewUser, getUserByLogin, getUserIdByName, getUserById # type: ignore 

env = Env()
env.read_env()

BOT_TOKEN = '7744140930:AAEtaKzDfFEls5-dc6KPMNui7Mzfv0zasiM'

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

#=================================Состояния диалогов=================================================================
class MainDialog(StatesGroup):
    start = State()
    task_list = State()
    show_task = State()

class TaskCreating(StatesGroup):
    title = State()
    description = State()
    accept = State()

class NotionCreating(StatesGroup):
    date = State()
    time = State()
    accept = State()

class SendNotion(StatesGroup):
    start = State()

#=================================Переходы между диалогами#===========================================================


async def go_main(
        callback: CallbackQuery, 
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.start(state=MainDialog.start, mode=StartMode.RESET_STACK)

async def to_notion(
        callback: CallbackQuery, 
        button: Button,
        dialog_manager: DialogManager):
    task_id = dialog_manager.dialog_data["task_id"]
    await dialog_manager.start(state=NotionCreating.date, data={"task_id": task_id})

async def create_task(
        callback: CallbackQuery, 
        button: Button,
        dialog_manager: DialogManager):
    await dialog_manager.start(state=TaskCreating.title)

async def change_task(
        callback: CallbackQuery, 
        button: Button,
        dialog_manager: DialogManager):
    title = dialog_manager.dialog_data["title"]
    description = dialog_manager.dialog_data["description"] 
    task_id = dialog_manager.dialog_data["task_id"]
    await dialog_manager.start(state=TaskCreating.accept, data={"task_id": task_id, "title": title, "description": description})


#=================================Стартеры маин диалога#===============================================================
# Это геттер
async def get_name(event_from_user: User, **kwargs):
    
    return {'user_name': event_from_user.first_name}

async def get_task_list(event_from_user: User, **kwargs):
    #await callback.message.answer(item_id)
    user_id = getUserByLogin(str(event_from_user.id))[0]["user_id"]
    resp = getTasksByUser(user_id)
    titles = []
    if resp:
        for i in resp:
            titles.append([i["title"],i["task_id"]])
    return {'tasks': resp, "titles": titles}

async def get_task(dialog_manager: DialogManager, **kwargs):
    #await callback.message.answer(item_id)
    if "task_id" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["task_id"] = dialog_manager.start_data["task_id"]
    task_id = dialog_manager.dialog_data["task_id"]
    #print(kwargs)
    resp = getTasksById(task_id)[0]
    dialog_manager.dialog_data["title"] = resp["title"]
    dialog_manager.dialog_data["description"] = resp["description"]
    dialog_manager.dialog_data["task_id"] = resp["task_id"]
    return {'task': resp["task_id"], "title": resp["title"], "description": resp["description"]}

#=================================Обработчики маин диалога#============================================================

async def delete_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    #await callback.message.answer(item_id)
    task_id = dialog_manager.dialog_data["task_id"]
    #print(kwargs)
    delTask(task_id)
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, task_id: int):
    dialog_manager.dialog_data["task_id"] = task_id
    await dialog_manager.next()

#=================================Стартеры создания таски#=============================================================

async def start_title(dialog_manager: DialogManager, **kwargs):
    if "title" not in dialog_manager.dialog_data:
        if  dialog_manager.start_data and "title" in dialog_manager.start_data:
            dialog_manager.dialog_data["title"] = dialog_manager.start_data["title"]
        else:
            dialog_manager.dialog_data["title"] = ''
    title = dialog_manager.dialog_data["title"]
    print(title)
    if "description" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["description"] = ''
    description = dialog_manager.dialog_data["description"]
    return {"title": title, "description": description}
    
async def start_description(dialog_manager: DialogManager, **kwargs):
    if "title" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["title"] = ''
    title = dialog_manager.dialog_data["title"]
    print(title)
    if "description" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["description"] = ''
    description = dialog_manager.dialog_data["description"]
    return {"title": title, "description": description}

async def start_accept(dialog_manager: DialogManager, **kwargs):
    if "title" not in dialog_manager.dialog_data:
        if  dialog_manager.start_data and "title" in dialog_manager.start_data:
            dialog_manager.dialog_data["title"] = dialog_manager.start_data["title"]
        else:
            dialog_manager.dialog_data["title"] = ''
    title = dialog_manager.dialog_data["title"]
    print(title)
    if "description" not in dialog_manager.dialog_data:
        if  dialog_manager.start_data and "description" in dialog_manager.start_data:
            dialog_manager.dialog_data["description"] = dialog_manager.start_data["description"]
        else:
            dialog_manager.dialog_data["description"] = ''
    description = dialog_manager.dialog_data["description"]
    return {"title": title, "description": description}


#=================================Сохранение таски#=====================================================================

async def save_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    print(callback.from_user.username, type(callback.from_user.username))
    user_id = getUserIdByName(callback.from_user.username)
    print(user_id)
    title = dialog_manager.dialog_data["title"]
    description = dialog_manager.dialog_data["description"]
    print(title, description)
    if dialog_manager.start_data and "task_id" in dialog_manager.start_data:
        task_id = dialog_manager.start_data["task_id"]
        updateTaskTitle(task_id, title)
        updateTaskDescription(task_id, description)
    else:
        task_id = addNewTask(user_id=user_id, title=title, description=description)
    print(task_id)
    await dialog_manager.start(state=MainDialog.show_task, data={"task_id": task_id})

#=================================Проверка юзер вавода для тасок#=======================================================

def title_check(text: str) -> str:
    if len(text) < 50:
        return text
    raise ValueError

def description_check(text: str) -> str:
    if len(text) < 250:
        return text
    raise ValueError

def time_check(text: str) -> str:
    resp = text.split(":")
    if len(resp) == 2:
        hour = resp[0]
        minute = resp[1]
        if not hour.isdigit() or not minute.isdigit():
            raise ValueError
        hour = int(hour)
        minute = int(minute)
        if hour > 24 or hour < 0:
            raise ValueError
        if minute > 60 or minute < 0:
            raise ValueError
        return text
    raise ValueError

async def correct_title_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    dialog_manager.dialog_data["title"] = text
    await dialog_manager.next()


async def quick_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    dialog_manager.dialog_data["title"] = text
    await dialog_manager.start(state=TaskCreating.accept, data={"title": text})

async def correct_description_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:
    dialog_manager.dialog_data["description"] = text
    await dialog_manager.next()

async def error_title_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Вы ввели слишком длинное название 😱 (подробно описать можно в описании задачи на следующем шаге)'
    )

async def error_description_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Вы ввели слишком длинное описание 😔 (я пока не могу столько запомнить)'
    )

async def error_time_handler(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        error: ValueError):
    await message.answer(
        text='Вы ввели время в неправильном формате 😱'
    )

async def no_text(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    #print(type(widget))
    await message.answer(text='Я пока могу обрабатывать только текст 😔')

#=================================Маин диалог#=========================================================================

start_dialog = Dialog(
    Window(                                                                        #--------Основное окно
        Format(text="Привет {user_name}😉"),
        Const(text="\n\n<i>Для быстрого создания, можно сразу ввести заголовок</i>"),
        Group(
            SwitchTo(Const("Список задач📋"), id='task_list', state=MainDialog.task_list),
            Button(Const("Создать задачу✏️"), id="crawl", on_click=create_task),
        ),
        TextInput(
            id='quick_input',
            on_success=quick_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        state=MainDialog.start,
        getter=get_name,
        parse_mode="HTML",
    ),
    Window(                                                                        #--------Окно списка задачь
        Const(text="<b>Список задач</b>"),
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
        Button(Const("Меню📖"), id="task", on_click=go_main),
        state=MainDialog.task_list,
        getter=get_task_list,
        parse_mode="HTML",
    ),
    Window(                                                                        #--------Окно просмотра задачи
        Format(text="<b>{title}</b>"),
        Format(text="{description}", when="description"),
        Group(
            Button(Const("Изменить✏️"), id="chang", on_click=change_task),
            Button(Const("Напоминание🕘"), id="notion", on_click=to_notion),
            Button(Const("Удалить ❌"), id="task", on_click=delete_task),
            width=3,
        ),
        SwitchTo(Const("Назад↩️"), id='task_list', state=MainDialog.task_list),
        state=MainDialog.show_task,
        getter=get_task,
        parse_mode="HTML",
    )
)


#=================================Создание таски#======================================================================

create_task = Dialog(
    Window(                                                                        #--------Ввод заголовка
        Format(text="Название: <b>{title}</b>", when="title"),
        Format(text="Описание: {description}", when="description"),
        Const(text="Введите название:"),
        Group(
            SwitchTo(Const("Готово ✅"), id='task_list', state=TaskCreating.accept, when="title"),
            SwitchTo(Const("Ввести описание"), id='task_list', state=TaskCreating.description, when="title"),
            Button(Const("Отмена ❌"), id="cancel", on_click=go_main),
            width=2,
        ),
        TextInput(
            id='title_input',
            type_factory=title_check,
            on_success=correct_title_handler,
            on_error=error_title_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        state=TaskCreating.title,
        getter=start_title,
        parse_mode="HTML",
    ),
    Window(                                                                        #--------Ввод описания
        Format(text="Название: <b>{title}</b>"),
        Format(text="Описание: {description}", when="description"),
        Const(text="Введи описание:"),
        Group(
            SwitchTo(Const("Готово ✅"), id='task_accept', state=TaskCreating.accept),
            SwitchTo(Const("Изменить название"), id='task_desc', state=TaskCreating.title),
            Button(Const("Отмена ❌"), id="cancel", on_click=go_main),
            width=2,
        ),
        TextInput(
            id='description_input',
            type_factory=description_check,
            on_success=correct_description_handler,
            on_error=error_description_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        state=TaskCreating.description,
        getter=start_description,
        parse_mode="HTML",
    ),
    Window(                                                                        #--------Подтверждение создания
        Const(text="Задача:"),
        Format(text="Название: <b>{title}</b>"),
        Format(text="Описание: {description}", when="description"),
        Group(
            SwitchTo(Const("Изменить название✏️"), id='title', state=TaskCreating.title),
            SwitchTo(Const("Изменить описание✏️"), id='task_desc', state=TaskCreating.description),
            Button(Const("Сохранить✅"), id='task_save', on_click=save_task),
            Button(Const("Отмена❌"), id="cancel", on_click=go_main),
            width=2,
        ),
        state=TaskCreating.accept,
        getter=start_accept,
        parse_mode="HTML",
    ),
    
)

async def get_date(dialog_manager: DialogManager, **kwargs):
    if "date" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["date"] = ''
    date = dialog_manager.dialog_data["date"]

    if "time" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["time"] = ''
    time = dialog_manager.dialog_data["time"]
    return {"date": date, "time": time, "nottime":  not time, "notdate": not date}

async def get_time(dialog_manager: DialogManager, **kwargs):
    if "date" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["date"] = ''
    date = dialog_manager.dialog_data["date"]

    if "time" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["time"] = ''
    time = dialog_manager.dialog_data["time"]
    return {"date": date, "time": time, "nottime":  not time, "notdate": not date}

async def notion_accept(dialog_manager: DialogManager, **kwargs):
    if "date" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["date"] = ''
    date = dialog_manager.dialog_data["date"]

    if "time" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["time"] = ''
    time = dialog_manager.dialog_data["time"]
    return {"date": date, "time": time, "nottime":  not time, "notdate": not date}

async def on_date_selected(callback: CallbackQuery, widget,
                           dialog_manager: DialogManager, selected_date: date):
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    date = datetime.strptime(str(selected_date), "%Y-%m-%d")
    print(date - now)
    if date < now:
        await callback.answer("Нельзя выбрать прошедшую дату")
    else:
        if date == now:
            dialog_manager.dialog_data["today"] = True
        else:
            dialog_manager.dialog_data["today"] = False
        dialog_manager.dialog_data["date"] = selected_date
        await dialog_manager.next()

# 2. Функция обработки выбора времени
async def on_time_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, time: str):
    now = datetime.now()
    date = dialog_manager.dialog_data["date"]
    res = f'{date} {time}'
    print(res)
    res = datetime.strptime(res, "%Y-%m-%d %H:%M")
    if res < now:
        await callback.answer("Нельзя выбрать прошедшее время")
        return
    dialog_manager.dialog_data["time"] = time
    await dialog_manager.next()  # Завершает диалог

async def save_notion(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    print(callback.from_user.username, type(callback.from_user.username))
    user_id = getUserIdByName(callback.from_user.username)
    print(user_id)
    date = dialog_manager.dialog_data["date"]
    time = dialog_manager.dialog_data["time"]
    result = f'{date} {time}'
    task_id = dialog_manager.start_data["task_id"]
    print(task_id, result, callback.message.chat.id)
    addNewNotion(task_id, result, callback.message.chat.id)
    print(task_id)
    await dialog_manager.done()

time_intervals = [f"{hour:02d}:{minute:02d}" for hour in range(0, 24) for minute in (0, 30)]

# Определяем диалог
notion_create = Dialog(
    Window(
        Multi(Format(text="Выбрана дата: <b>{date}</b>", when="date"), Format(text="время: <b>{time}</b>", when="time"), sep =" "),
        Const("Измените дату уведомления:", when="date"),
        Const("Выберите дату уведомления:", when="notdate"),
        Calendar(id='calendar', on_click=on_date_selected),  # Используем простой календарь
        SwitchTo(Const("Оставить"), id='title', state=NotionCreating.time, when="date"),
        Button(Const("Отмена ❌"), id="cancel", on_click=go_main),
        state=NotionCreating.date,
        getter=get_date,
        parse_mode="HTML",
    ),
    Window(
        Multi(Format(text="Выбрана дата: <b>{date}</b>", when="date"), Format(text="время: <b>{time}</b>", when="time"), sep =" "),
        Const("Измените время уведомления:", when="time"),
        Const("Выберите время уведомления:", when="nottime"),
        Const("\n<i>Или отправьте в формате ЧЧ:ММ</i>"),
        ScrollingGroup(
            Select(
                text=Format("{item}"),
                id="time_select",
                items=time_intervals,  # Список интервалов времени
                item_id_getter=lambda x: x,  # ID кнопки = текст кнопки
                on_click=on_time_selected,  # Обработчик выбора
            ),
            id = "scroll",
            width=4,  # Количество кнопок в строке
            height=6,  # Количество строк
        ),
        TextInput(
            id='description_input',
            type_factory=time_check,
            on_success=on_time_selected,
            on_error=error_time_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY
        ),
        SwitchTo(Const("Оставить"), id='title', state=NotionCreating.accept, when="time"),
        Button(Const("Отмена ❌"), id="cancel", on_click=go_main),
        state=NotionCreating.time,
        getter=get_time,
        parse_mode="HTML",
    ),
    Window(                                                                        #--------Подтверждение создания
        Multi(Format(text="Выбрана дата: <b>{date}</b>", when="date"), Format(text="время: <b>{time}</b>", when="time"), sep =" "),
        Group(
            SwitchTo(Const("Изменить дату📆"), id='title', state=NotionCreating.date),
            SwitchTo(Const("Изменить время🕘"), id='task_desc', state=NotionCreating.time),
            Button(Const("Сохранить✅"), id='task_save', on_click=save_notion),
            Button(Const("Отмена❌"), id="cancel", on_click=go_main),
            width=2,
        ),
        state=NotionCreating.accept,
        getter=notion_accept,
        parse_mode="HTML",
    ),
)

notion = Dialog(
    Window(                                                                        #--------Подтверждение создания
        Const(text="Задача:"),
        Format(text="Название: <b>{title}<b>"),
        Format(text="Описание: {description}", when="description"),
        Group(
            Cancel(Const("Назад↩️")),
            Button(Const("Меню📖"), id="cancel", on_click=go_main),
            width=2,
        ),
        state=SendNotion.start,
    ),
)

router = Router()

# Этот классический хэндлер будет срабатывать на команду /start
@router.message(Command("start"))
async def command_start_process(message: Message, dialog_manager: DialogManager):
    addNewUser (str(message.from_user.id), str(message.from_user.username))
    await dialog_manager.start(state=MainDialog.start, mode=StartMode.RESET_STACK)

if __name__ == "__main__":
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)
