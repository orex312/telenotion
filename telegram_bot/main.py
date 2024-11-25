# Тестовый бот с минимальной разметкой и кнопочками
#  https://habr.com/ru/articles/732136/
# 7767052229:AAGcy1tK09SyCAXXz17Uso41WSYQqD-RxRM



import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode #       -- содержит настройки разметки сообщений (HTML, Markdown)
from aiogram.fsm.storage.memory import MemoryStorage # -- хранилища данных для состояний пользователей
from aiogram import BaseMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler




from handlers import router # type: ignore 

class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self,handler,event,data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)

# Удалено чтение токена из файла, пока хз почему не работает
API_TOKEN = '7744140930:AAEtaKzDfFEls5-dc6KPMNui7Mzfv0zasiM'
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)

async def main():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    dp.include_router(router)
    from notions.notions import notion, notion_old
    await notion_old()
    scheduler.add_job(notion,'cron',second=0)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())









