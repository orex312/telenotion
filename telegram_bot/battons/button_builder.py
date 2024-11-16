from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import os
import sys

sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))

#from user_operations import addNewUser, getUserByLogin # type: ignore 
from tasks_operations import getTasksByUser, addNewTask, updateTaskDescription, getTasksById, delTask # type: ignore
from state_operations import getUserState, updateUserState # type: ignore





def but_builder(state, tasks = []):
    keyboard = []

    match state:

        case "createTask": 
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
        case "main_menu": 
            keyboard.append([InlineKeyboardButton(text='Список задач', callback_data="show")])
            keyboard.append([InlineKeyboardButton(text='Новая задача', callback_data="new_task")])
        case "showAll": 
            i = 1
            for task in tasks:
                btn = InlineKeyboardButton(text=str(i)+". " + task['title'], callback_data="task_"+str(task['task_id']))
                keyboard.append([btn])
                i += 1
        case "task": 
            keyboard.append([InlineKeyboardButton(text='Список задач', callback_data="show")])
            keyboard.append([InlineKeyboardButton(text='Новая задача', callback_data="new_task")])
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
        case _:
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
        
    return InlineKeyboardMarkup(inline_keyboard = keyboard)