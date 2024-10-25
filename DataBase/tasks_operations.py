from connection import Connection
from datetime import date

connect = Connection().connect
try:
    def addNewTask(login, name):
        with connect.cursor() as cursor:
            query = '''SELECT * FROM Users
                        WHERE login = %s'''
            cursor.execute(query, [login])
            if cursor.fetchall():
                return "user with this login already exist"
            query = '''INSERT INTO Users (login, user_name, creatad_at)
                        VALUES (%s,%s,%s)'''
            cursor.execute(query, [login, name, date.today()])

    def getAllUsers():
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Users) FROM Users'''
            cursor.execute(query)
            response = cursor.fetchall()
            return response[0][0]
        
    def getUserByLogin(login):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Users) FROM Users
                    WHERE login = %s'''
            cursor.execute(query,[login])
            response = cursor.fetchall()
            return response[0][0]
        
    def getUserById(id):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Users) FROM Users
                    WHERE user_id = %s'''
            cursor.execute(query,[id])
            response = cursor.fetchall()
            return response[0][0]

except Exception as _ex:
        print("[INFO][tasks_operations] Error while working with PostgreSQL", _ex)