from connection import Connection
from user_operations import *
from tasks_operations import *

user_name = "Alex"
user_login = "Apelsin312"

title = "Test"
description = "Dopustin tak"

# Добавить нового юзера
resp = addNewUser(user_login, user_name)
if resp:
    print(resp)
'''
# Список всех юзеров
resp = getAllUsers()
for i in resp:
    print(f'Имя: {i["user_name"]}, логин: {i["login"]}, дата создания: {i["creatad_at"]}')

# Юзер по ID
resp = getUserById(1)
for i in resp:
    print(f'Имя: {i["user_name"]}, логин: {i["login"]}, дата создания: {i["creatad_at"]}')

# Юзер по логину
resp = getUserByLogin(user_login)
for i in resp:
    print(f'Имя: {i["user_name"]}, логин: {i["login"]}, дата создания: {i["creatad_at"]}')
    '''
#resp = addNewTask(user_login, title, description, parent_id=1)
#if resp:
#    print(resp)

resp = getTasksByUser(user_login)
print(resp)
for i in resp:
    print(f'title - {i['title']} \decription - {i['description']} \ due_date - {i['due_date']}')
    t1 = getSubTasks(i['task_id'])
    if t1:
        print(f'    SubTasks of {i['title']}:')
        for j in t1:
            print(f'    title - {j['title']} \decription - {j['description']} \ due_date - {j['due_date']}')



