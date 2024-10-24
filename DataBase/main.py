from connection import Connection
from basic_operations import *

user_name = "Alex"
User_login = "Apelsin312"
addNewUser(User_login, user_name)
resp = getAllUsers()
for i in resp:
    print(i["user_name"],i["user_login"],i["creatad_at"])