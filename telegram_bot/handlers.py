import os
import sys
from logic.task import taskCreating # type: ignore
sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))


from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from user_operations import addNewUser, getUserByLogin # type: ignore 
from state_operations import addUserState, getUserStateByLogin, getUserState, updateUserState # type: ignore
#from state_operations import getUserState # type: ignore


import kb
import text

router = Router()



@router.message(Command("Хто_я"))
async def message_test(msg: Message):
    addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    resp = getUserByLogin (str(msg.from_user.id)) [0]
    await msg.answer(resp["user_name"])





@router.message(Command("task"))
async def task_handler(msg: Message):
    user_id = addNewUser(str(msg.from_user.id), str(msg.from_user.username))
    print(user_id)
    addUserState(user_id)
    updateUserState(user_id, step = "createTask")
    await msg.answer("Введи название задачи")






@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(Command("qwe"))
async def message_to_any (msg:Message):
    await msg.answer ("Неизвестная комманда\n")

@router.message(Command("rty"))
async def message_handler(msg: Message):
    await msg.answer(f"{msg.text}")

@router.message()
async def message_test(msg: Message):
    user_id = addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    user_state = getUserState(user_id)
    print(user_state)
    step = user_state["curent_step"]
    context = user_state["context"]
    match step:
        case "createTask":
            text = taskCreating(user_id, context, msg.text)
            if text: await msg.answer(text)

        case "main_menu":
            resp = getUserByLogin (str(msg.from_user.id)) [0]
            print("hui")
            await msg.answer(str(resp["user_id"]))
            await msg.answer(resp["user_name"])


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
# @router.message()

async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
