from connection import Connection
from datetime import date

connect = Connection().connect

def addNewUser(login, name):
    try:
        with connect.cursor() as cursor:
            query = '''SELECT * FROM Users
                        WHERE login = %s'''
            cursor.execute(query, [login])
            if cursor.fetchall():
                 return "user with this login already exist"
            query = '''INSERT INTO Users (login, user_name, creatad_at)
                        VALUES (%s,%s,%s)'''
            cursor.execute(query, [login, name, date.today()])
    except Exception as _ex:
        print("[INFO][addNewUser] Error while working with PostgreSQL", _ex)

def getAllUsers():
    try:
        with connect.cursor() as cursor:
                query = '''SELECT json_agg(Users) FROM Users'''
                cursor.execute(query)
                response = cursor.fetchall()
                return response[0]
    except Exception as _ex:
        print("[INFO][getAllUsers] Error while working with PostgreSQL", _ex)