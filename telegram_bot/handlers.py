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



@router.message(Command("Хто_я"))
async def message_test(msg: Message):
    addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    resp = getUserByLogin (str(msg.from_user.id)) [0]
    await msg.answer(resp["user_name"])


@router.message()
async def message_test(msg: Message):
    addNewUser (str(msg.from_user.id), str(msg.from_user.username))
    resp = getUserByLogin (str(msg.from_user.id)) [0]
    await msg.answer(str(resp["user_id"]))
    await msg.answer(resp["user_name"])











@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(Command("qwe"))
async def message_to_any (msg:Message):
    await msg.answer ("Неизвестная комманда\n")

@router.message(Command("rty"))
async def message_handler(msg: Message):
    await msg.answer(f"{msg.text}")


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
# @router.message()

async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
