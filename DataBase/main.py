from connection import Connection
from basic_operations import *

user_name = "Alex"
User_login = "Apelsin312"
resp = addNewUser(User_login, user_name)
if resp:
    print(resp)
resp = getAllUsers()[0]
#print(resp[0])
for i in resp:
    print(f'Имя: {i["user_name"]}, логин: {i["login"]}, дата создания: {i["creatad_at"]}')