import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode #       -- содержит настройки разметки сообщений (HTML, Markdown)
from aiogram.fsm.storage.memory import MemoryStorage # -- хранилища данных для состояний пользователей
from aiogram import BaseMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram.types import CallbackQuery
from aiogram import Bot, types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
import bot_config




class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self,handler,event,data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)

# Удалено чтение токена из файла, пока хз почему не работает
API_TOKEN = bot_config.main_bot_token
bot = Bot(token=API_TOKEN)


async def main():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    from dialogs import router, start_dialog, create_task, notion_create
    from dialog_with_user import donate_dialog
    dp.include_routers(router, start_dialog, create_task, notion_create, donate_dialog)
    setup_dialogs(dp)
    from notions.notions import notion, notion_old
    await notion_old()
    scheduler.add_job(notion,'cron',second=0)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())