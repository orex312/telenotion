from connection import Connection
from user_operations import *
from tasks_operations import *
from state_operations import *

user_name = "Ilya"
user_login = "Pipiska"

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
#resp = addNewTask(user_login, title, description, parent_id=5)
#if resp:
#    print(resp)

resp = getUserStateByLogin(user_login)
#print(resp)
for i in resp:
    print(i)



