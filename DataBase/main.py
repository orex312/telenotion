from connection import Connection
from user_operations import *

user_name = "Ilya"
user_login = "Pipiska"

# Добавить нового юзера
resp = addNewUser(user_login, user_name)
if resp:
    print(resp)

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