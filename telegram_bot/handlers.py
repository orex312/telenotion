from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import kb
import text

router = Router()

@router.message()
async def message_to_any (msg:Message):
    await msg.answer ("Неизвестная комманда\n"+
                      "используй /help")


@router.message(Command("help"))
async def message_to_any (msg:Message):
    await msg.answer ("Доступные комманды:\n" +
                      "/help  - хелп, он и в Африке Хэлп\n" +
                      "/start - приветственное сообщение\n" +
                      "/ID    - узнать твой ID")

"""
@router.message(Command("hello"))
async def message_hello (msg:Message):
    await msg.answer("Привет!\n")


@router.message(Command("ID"))
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
"""

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)




@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
# @router.message()

async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
