from connection import Connection
from datetime import date

connect = Connection().connect

def addNewUser(login, name):
    try:
        with connect.cursor() as cursor:
            query = '''INSERT INTO Users (login, user_name, creatad_at)
                        VALUES (%s,%s,%s)'''
            cursor.execute(query, [login, name, date.today()])
    except Exception as _ex:
        print("[INFO][addNewUser] Error while working with PostgreSQL", _ex)

def getAllUsers():
    try:
        with connect.cursor() as cursor:
                query = '''SELECT * FROM Users'''
                cursor.execute(query)
                response = cursor.fetchall()
                return response
    except Exception as _ex:
        print("[INFO][getAllUsers] Error while working with PostgreSQL", _ex)