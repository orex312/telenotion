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





def but_builder(state, context = None, resp = [], rng = 1, task_id = None):
    keyboard = []

    match state:

        case "createTask": 
            if context:
                task_id = context.split()[1]
                keyboard.append([InlineKeyboardButton(text='Готово', callback_data="task_"+str(task_id))])
            else:
                keyboard.append([InlineKeyboardButton(text='Отмена', callback_data="kb")])
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
        case "main_menu": 
            keyboard.append([InlineKeyboardButton(text='Список задач', callback_data="show")])
            keyboard.append([InlineKeyboardButton(text='Новая задача', callback_data="new_task")])
        case "showAll": 
            i = rng
            if resp:
                for k in range(i-1,len(resp)):
                    btn = InlineKeyboardButton(text=str(i)+". " + resp[k]['title'], callback_data="task_"\
                                               +str(resp[k]['task_id']))
                    btn2 = InlineKeyboardButton(text=resp[k]['status'], callback_data="_")
                    btn3 = InlineKeyboardButton(text="☑️", callback_data="taskOk_"+str(resp[k]['task_id']))
                    btn4 = InlineKeyboardButton(text="❌", callback_data="del_"+str(resp[k]['task_id']))
                    keyboard.append([btn])
                    keyboard.append([btn2,btn3,btn4])
                    print(i)
                    if i%5 == 0:
                        break
                    i += 1
                nxt = InlineKeyboardButton(text='▶️', callback_data="show_" + str(i+1))
                prev = InlineKeyboardButton(text='◀️', callback_data="show_" + str(rng-5))
                rsp = []
                if i > 5:
                    rsp.append(prev)
                
                if i < len(resp):
                    rsp.append(nxt)
                keyboard.append(rsp)
                        
                    
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
        case "task": 
            btn = InlineKeyboardButton(text='❌', callback_data="del")
            btn2 = InlineKeyboardButton(text='Напоминание', callback_data="remind_"+str(task_id))
            btn3 = InlineKeyboardButton(text="☑️", callback_data="taskOk_"+str(task_id))
            keyboard.append([btn2,btn3,btn])
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
        case "remind":  
            btn = InlineKeyboardButton(text='↩️', callback_data="task_"+str(task_id))
            btn3 = InlineKeyboardButton(text='Новая задача', callback_data="new_task")
            keyboard.append([btn, btn3])
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
        case _:
            keyboard.append([InlineKeyboardButton(text='Меню', callback_data="kb")])
    return InlineKeyboardMarkup(inline_keyboard = keyboard)