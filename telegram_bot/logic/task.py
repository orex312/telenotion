import os
import sys

sys.path.insert (1, os.path.join (sys.path[0], "../DataBase"))

#from user_operations import addNewUser, getUserByLogin # type: ignore 
from tasks_operations import addNewTask, updateTaskDescription # type: ignore
from state_operations import getUserState, updateUserState # type: ignore





def taskCreating(user_id, context, msg):
    
    print(user_id, context)
    print(msg)
    if not context:
        task_id = addNewTask(user_id, msg)
        updateUserState(user_id, step = "createTask", context = f"title {task_id}")
        return "Введи описание задачи"
    context = context.split()
    match context[0]:
        case "title":
            updateTaskDescription(context[1], msg)
            updateUserState(user_id)
            return "Готово"

