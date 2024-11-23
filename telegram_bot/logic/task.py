import os
import sys

sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))

#from user_operations import addNewUser, getUserByLogin # type: ignore 
from tasks_operations import addNewTask, updateTaskDescription, getTasksById, delTask # type: ignore
from state_operations import getUserState, updateUserState # type: ignore

def showTask(user_id, task_id):
    resp = getTasksById(task_id)
    #return not resp
    if not resp or (resp[0]['user_id'] != user_id):
        return 'Нет задачи с таким номером'
    resp = resp[0]
    updateUserState(user_id, "task", task_id)
    text = f'Номер-{task_id}\nНазвание: {resp['title']}\nОписание: {resp['description']}'
    return text

def taskShows(user_id, context, msg):
    print(user_id, context)
    print(msg)
    msg = msg.split()
    match msg[0]:
        case '/del':
            if len(msg) == 1:
                return 'Не введен номер задачи для уаления'
            resp = getTasksById(msg[1])[0]
            if not resp or (resp['user_id'] != user_id):
                return 'Введен номер несуществующей задачи'
            delTask(msg[1])
        case _ :
            return 0

    return 'Задача удалена'

def taskCreating(user_id, context, msg):
    
    #print(user_id, context)
    #print(msg)
    if not context:
        task_id = addNewTask(user_id, str(msg))
        updateUserState(user_id, step = "createTask", context = f"title {task_id}")
        return "Введи описание задачи"
    context = context.split()
    match context[0]:
        case "title":
            updateTaskDescription(context[1], msg)
            return '\n'.join(["Готово",showTask(user_id, context[1])])
        case _ :
            return '\n'.join(["Готово",showTask(user_id, context[1])])



