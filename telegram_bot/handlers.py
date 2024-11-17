import os
import sys
from aiogram.types import CallbackQuery
from battons.button_builder import but_builder

from logic.task import taskCreating, taskShows, showTask # type: ignore
sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))


from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from user_operations import addNewUser, getUserByLogin, getUserIdByName, getUserById # type: ignore 
from state_operations import addUserState, getUserStateByLogin, getUserState, updateUserState # type: ignore
from tasks_operations import getTasksByUser, getTasksById, delTask, updateTaskDate # type: ignore


import kb
import text

router = Router()


@router.message(F.text.in_({"/kb","Меню"}))
async def message_test(msg: Message):
    user_id = addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    updateUserState(user_id, step = "main_menu")
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    resp = getUserByLogin (str(msg.from_user.id)) [0]
    await msg.edit_text(text.main_menu(resp["user_name"]), reply_markup=but_builder(step))

@router.callback_query (F.data == "kb")
async def message_test(call: CallbackQuery):
    msg = call.message
    user_id = getUserIdByName(call.message.chat.username)
    updateUserState(user_id, step = "main_menu")
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    resp = getUserById (user_id) [0]
    await msg.edit_text(text.main_menu(resp["user_name"]), reply_markup=but_builder(step))

@router.message(Command("start"))
async def start_handler(msg: Message):
    user_id = addNewUser(str(msg.from_user.id), str(msg.from_user.username))
    print(user_id)
    updateUserState(user_id, step = "main_menu")
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    resp = getUserById (user_id) [0]
    await msg.answer(text.main_menu(resp["user_name"]), reply_markup=but_builder(step))

@router.callback_query (F.data.startswith('task_'))
async def test (call: CallbackQuery):
    task_id = call.data.split("_")[1]
    user_id = getUserIdByName(call.message.chat.username)
    updateUserState(user_id, step = "task", context = "show "+ str(task_id))
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    task = getTasksById(task_id)[0]
    if task['description']:
        await call.message.edit_text(f'Название: {task['title']}\nОписание: {task['description']}',\
                                  reply_markup=but_builder(step))
    else:
        await call.message.edit_text(f'Название: {task['title']}',\
                                  reply_markup=but_builder(step))

@router.callback_query (F.data.startswith('taskOk_'))
async def test (call: CallbackQuery):
    task_id = call.data.split("_")[1]
    user_id = getUserIdByName(call.message.chat.username)
    user_state = getUserState(user_id)
    updateTaskDate(task_id, "done")
    await call.answer("Задача помечена как сделанная")

@router.callback_query (F.data.startswith('del_'))
async def test (call: CallbackQuery):
    task_id = call.data.split("_")[1]
    user_id = getUserIdByName(call.message.chat.username)
    step = getUserState(user_id)
    resp = getTasksById(task_id)
    if not resp or (resp[0]['user_id'] != user_id):
        await call.answer("Введен номер несуществующей задачи")
        return 'Введен номер несуществующей задачи'
    delTask(task_id)
    await call.answer("Задача удалена")
    resp = getTasksByUser(user_id)
    if resp:
        await call.message.edit_text("Твои задачи:",reply_markup=but_builder(step,resp=resp))
    else:
        await call.message.edit_text("Список задач пуст😊",reply_markup=but_builder(step,resp=resp))

@router.callback_query (F.data == "del")
async def message_test(call: CallbackQuery):
    msg = call.message
    user_id = getUserIdByName(call.message.chat.username)
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    context = user_state["context"]
    task_id = context.split()[1]
    resp = getTasksById(task_id)
    if not resp or (resp[0]['user_id'] != user_id):
        await msg.edit_text ("Введен номер несуществующей задачи\n", reply_markup=but_builder('main_menu'))
        return 'Введен номер несуществующей задачи'
    delTask(task_id)
    updateUserState(user_id, step = "main_menu")
    await msg.edit_text ("Задача удалена\n", reply_markup=but_builder('main_menu'))
    

@router.callback_query (F.data == "new_task")
async def test (call: CallbackQuery):
    msg = call.message
    user_id = getUserIdByName(msg.chat.username)
    updateUserState(user_id, step = "createTask")
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    await msg.edit_text("Введи название задачи",reply_markup=but_builder(step))

@router.callback_query (F.data == "show_tasks")
async def test (call: CallbackQuery):
    msg = call.message
    user_id = getUserIdByName(msg.chat.username)
    #print(user_id)
    updateUserState(user_id, step = "showAll")
    resp = getTasksByUser(user_id)
    if not resp:
        await msg.edit_text ("Нет задач\n")
        return 0
    for task in resp:
        await msg.edit_text(f'Номер-{task['task_id']}\nНазвание: {task['title']}\nОписание: {task['description']}')
    if len(resp) == 1:
        updateUserState(user_id, "task", resp[0]['task_id'])


@router.callback_query (F.data.startswith('show'))
async def test (call: CallbackQuery):
    msg = call.message
    show = call.data.split("_")
    if len(show) > 1:
        rng = int(show[1])
    else:
        rng = 1
    print(rng)
    user_id = getUserIdByName(msg.chat.username)
    updateUserState(user_id, step = "showAll")
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    resp = getTasksByUser(user_id)
    if resp:
        await msg.edit_text("Твои задачи:",reply_markup=but_builder(step,resp=resp,rng=rng))
    else:
        await msg.edit_text("Список задач пуст😊",reply_markup=but_builder(step,resp=resp,rng=rng))



@router.message(Command("help"))
async def help_handler(msg: Message):
    addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    await msg.answer(
"""Команды:
/task - создать задачу
/show [номер задачи] - вывод всех задач(или по номеру)
/del [номер задачи] - удаление текующей задачи(по номеру задачи)""")

@router.message(Command("Хто_я"))
async def message_test(msg: Message):
    addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    resp = getUserByLogin (str(msg.from_user.id)) [0]
    await msg.answer(text.main_menu(resp["user_name"]), reply_markup=kb.main_menu)

@router.message(Command("task"))
async def task_handler(msg: Message):
    user_id = addNewUser(str(msg.from_user.id), str(msg.from_user.username))
    print(user_id)
    updateUserState(user_id, step = "createTask")
    await msg.answer("Введи название задачи")



@router.message(Command("del"))
async def del_handler (msg:Message):
    user_id = addNewUser(str(msg.from_user.id), str(msg.from_user.username))
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    context = user_state["context"]
    text = msg.text.split()
    if len(text) == 2:
        if not text[1].isdigit():
            await msg.answer ("Введен номер несуществующей задачи\n")
            return 'Введен номер несуществующей задачи'
        resp = getTasksById(text[1])
        if not resp or (resp[0]['user_id'] != user_id):
            await msg.answer ("Введен номер несуществующей задачи\n")
            return 'Введен номер несуществующей задачи'
        delTask(text[1])
        await msg.edianswert_text ("Задача удалена\n")
    elif len(text) == 1:
        if step == 'task' and context:
            resp = getTasksById(context)[0]
            if not resp or (resp['user_id'] != user_id):
                return 'Введен номер несуществующей задачи'
            delTask(context)
            await msg.answer ("Задача удалена\n")
    else:
        await msg.answer ("Неизвестная команда\n")

@router.message(Command("rty"))
async def message_handler(msg: Message):
    await msg.answer(f"{msg.text}")

@router.message(Command("show"))
async def show_handler(msg: Message):
    user_id = addNewUser(str(msg.from_user.id), str(msg.from_user.username))
    updateUserState(user_id, step = "showAll")
    text = msg.text.split()
    if len(text) == 2:
        if not text[1].isdigit():
            await msg.answer ("Введен номер несуществующей задачи\n")
            return 'Введен номер несуществующей задачи'
        resp = showTask(user_id, text[1])
        await msg.answer(str(resp))
    else:
        resp = getTasksByUser(user_id)
        if not resp:
            await msg.answer ("Нет задач\n")
            return 0
        for task in resp:
            await msg.answer(f'Номер-{task['task_id']}\nНазвание: {task['title']}\nОписание: {task['description']}')
        if len(resp) == 1:
            updateUserState(user_id, "task", resp[0]['task_id'])

@router.message()
async def message_handler(msg: Message):
    user_id = addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    user_state = getUserState(user_id)
    step = user_state["curent_step"]
    context = user_state["context"]
    match step:
        case "createTask":
            text = taskCreating(user_id, context, msg.text)
            user_state = getUserState(user_id)
            step = user_state["curent_step"]
            context = user_state["context"]
            if text: await msg.answer(text,reply_markup=but_builder(step, context=context))

        case "showAll":
            text = taskShows(user_id, context, msg.text)
            if text: await msg.answer(text)
        case "main_menu":
            resp = getUserByLogin (str(msg.from_user.id)) [0]
            print("hui")
            await msg.answer(str(resp["user_id"]))
            await msg.answer(resp["user_name"])


