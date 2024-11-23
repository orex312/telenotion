from connection import Connection
from datetime import date, datetime

connect = Connection().connect
try:
    def addNewUser(login, name):
        with connect.cursor() as cursor:
            query = '''SELECT user_id FROM Users
                        WHERE login = %s'''
            cursor.execute(query, [login])
            response = cursor.fetchall()
            if response:
                if response:
                    return response[0][0]
            query = '''INSERT INTO Users (login, user_name, creatad_at)
                        VALUES (%s,%s,%s)'''
            cursor.execute(query, [login, name, date.today()])
            query = '''SELECT user_id FROM Users
                        WHERE login = %s'''
            cursor.execute(query, [login])
            response = cursor.fetchall()
            query = '''INSERT INTO User_State (user_id, last_updated)
                        VALUES (%s,%s)'''
            cursor.execute(query, [response[0][0], datetime.now()])
            if response:
                return response[0][0]

    def getAllUsers():
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Users) FROM Users'''
            cursor.execute(query)
            response = cursor.fetchall()
            if response:
                return response[0][0]
        
    def getUserByLogin(login):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Users) FROM Users
                    WHERE login = %s'''
            cursor.execute(query,[login])
            response = cursor.fetchall()
            if response:
                return response[0][0]
        
    def getUserIdByName(user_name):
        with connect.cursor() as cursor:
            query = '''SELECT user_id FROM Users
                    WHERE user_name = %s'''
            cursor.execute(query,[user_name])
            response = cursor.fetchall()
            if response:
                return response[0][0]
        
    def getUserById(id):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Users) FROM Users
                    WHERE user_id = %s'''
            cursor.execute(query,[id])
            response = cursor.fetchall()
            if response:
                return response[0][0]

except Exception as _ex:
        print("[INFO][user_operations] Error while working with PostgreSQL", _ex)