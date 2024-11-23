import os
import sys
from aiogram.types import CallbackQuery
from battons.button_builder import but_builder
from datetime import date, datetime
from battons.button_builder import but_builder

from logic.task import taskCreating, taskShows, showTask # type: ignore
sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))


from aiogram import Bot, types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from user_operations import addNewUser, getUserByLogin, getUserIdByName, getUserById # type: ignore 
from state_operations import addUserState, getUserStateByLogin, getUserState, updateUserState # type: ignore
from tasks_operations import getTasksByUser, getTasksById, delTask, updateTaskDate # type: ignore
from notion_operations import addNewNotion, delNotion, getActiveNotions, updateNotion, getNotActiveNotions # type: ignore

#нужно установить пакет apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import BaseMiddleware

scheduler = AsyncIOScheduler()

async def send_notion(chat_id, task_id):
    from main import bot as bt
    task = getTasksById(task_id)[0]
    if task['description']:
        await bt.send_message(chat_id=chat_id,text=
                            f'УВЕДОМЛЕНИЕ\nНазвание: {task['title']}\nОписание: {task['description']}',
                            reply_markup=but_builder("task", task_id=task['task_id']))
    else:
        await bt.send_message(chat_id=chat_id,text=\
                              f'УВЕДОМЛЕНИЕ\nНазвание: {task['title']}',
                              reply_markup=but_builder("task", task_id=task['task_id']))



async def notion():
    date_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
    notions = getActiveNotions(date_time)
    print(notions, date_time)
    if notions:
        for notion in notions:
            await send_notion(notion['chat_id'], notion['task_id'])
            updateNotion(notion['reminder_id'])

async def notion_old():
    date_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
    notions = getNotActiveNotions(date_time)
    print(notions, date_time)
    if notions:
        for notion in notions:
            await send_notion(notion['chat_id'], notion['task_id'])
            updateNotion(notion['reminder_id'])


