from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import kb
import text

router = Router()



@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message()
async def message_to_any (msg:Message):
    await msg.answer ("Неизвестная комманда\n"+
                      "используй /help")


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
# @router.message()

async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
