import os
import sys
sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from user_operations import addNewUser, getUserByLogin # type: ignore 

import kb
import text

router = Router()

@router.message(Command("start"))
async def message_test(msg: Message):
    addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    resp = getUserByLogin (str(msg.from_user.id)) [0]
    await msg.answer(text.main_menu(resp["user_name"]), reply_markup=kb.main_menu)


@router.message()
async def my_tasks(msg: Message):
    addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    resp = getUserByLogin (str(msg.from_user.id)) [0]
    await msg.answer(text.main_menu(resp["user_name"]), reply_markup=kb.new_tasks_menu)



@router.message()
async def start_handler(msg: Message):
    await msg.answer("Неизвестная комманда")


