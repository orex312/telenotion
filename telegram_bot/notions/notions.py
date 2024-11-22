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


#нужно установить пакет apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import BaseMiddleware

scheduler = AsyncIOScheduler()

router = Router()
## позволяет доставать scheduler из агрументов фунции
class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self,handler,event,data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


@router.message(Command("send"))
async def start_handler(msg: Message, bot: Bot, scheduler: AsyncIOScheduler):
    user_id = addNewUser(str(msg.from_user.id), str(msg.from_user.username))
    id = msg.from_user.id
    print(id)
    user_state = getUserState(user_id)
    # задаём выполнение задачи в равные промежутки времени
    scheduler.add_job(bot.send_message,'interval',seconds=20 ,args=(id,"Я напоминаю каждые 20 секунд"))
    # задаём выполнение задачи по cron - гибкий способ задавать расписание. Подробнеее https://crontab.guru/#8_*_*_4
    scheduler.add_job(bot.send_message,'cron',hour=1,minute=10,args=(id,"Я напомнил в 1.10 по Москве"))


