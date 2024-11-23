from connection import Connection
from datetime import date, datetime
from user_operations import *

connect = Connection().connect
try:
    def addUserState(id):
        with connect.cursor() as cursor:
            query = '''SELECT * FROM User_state
                        WHERE user_id = %s'''
            cursor.execute(query, [id])
            if cursor.fetchall():
                return "user state already exist"
            query = '''INSERT INTO User_State (user_id, last_updated)
                        VALUES (%s,%s)'''
            cursor.execute(query, [id, datetime.now()])

    def getUserState(id):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(User_State) FROM User_State
                        WHERE user_id = %s'''
            cursor.execute(query, [id])
            response = cursor.fetchall()
            if response and response[0] and response[0][0] and response[0][0][0]:
                return response[0][0][0]
        
    def getUserStateByLogin(login):
        id = getUserByLogin(login)[0]["user_id"]
        return getUserState(id)
        
    def updateUserState(id, step = "main_menu", context = None):
        with connect.cursor() as cursor:
            query = '''UPDATE User_State
                        SET curent_step = %s,
                        context = %s,
                        last_updated = %s
                        WHERE user_id = %s'''
            cursor.execute(query,[step, context, datetime.now(), id])
            return None

except Exception as _ex:
        print("[INFO][state_operations] Error while working with PostgreSQL", _ex)