from connection import Connection
from datetime import date
from user_operations import *

connect = Connection().connect
try:
    # Создание новой напоминалки
    def addNewNotion(task_id, remind_at, chat_id):
        with connect.cursor() as cursor:
            query = '''select max(reminder_id) from Reminders'''
            cursor.execute(query)
            reminder_id = cursor.fetchall()[0][0]
            print(reminder_id)
            if reminder_id == None:
                reminder_id = 1
            else:
                reminder_id += 1
            query = '''INSERT INTO Reminders (reminder_id, task_id, remind_at, chat_id)
                        VALUES (%s,%s,%s,%s)'''
            cursor.execute(query, [reminder_id, int(task_id), remind_at, int(chat_id)])
            return reminder_id

#---------------------------------------------------------------

# Удалить напоминалку             
    def delNotion(task_id):
        with connect.cursor() as cursor:
            query = '''UPDATE Reminders
                        SET sent = True
                        WHERE task_id = %s'''
            cursor.execute(query,[task_id])
            return 0
    
#-----------------------Получение напоминалок-------------------------
    
# Получить все напминалки по времени    
    def getActiveNotions(remind_at):
        with connect.cursor() as cursor:
            query = '''With temp as (
                            SELECT r.task_id as task_id, r.chat_id as chat_id, reminder_id
                                FROM Reminders r JOIN Tasks t ON r.task_id = t.task_id
                                    and remind_at = %s and sent = False)
                        select json_agg(temp) FROM temp'''
            cursor.execute(query,[remind_at])
            response = cursor.fetchall()
            if response and response[0] and response[0][0]:
                return response[0][0]
            return None
    
    def getNotActiveNotions(remind_at):
        with connect.cursor() as cursor:
            query = '''With temp as (
                            SELECT r.task_id as task_id, r.chat_id as chat_id, reminder_id
                                FROM Reminders r JOIN Tasks t ON r.task_id = t.task_id
                                    and remind_at <= %s and sent = False)
                        select json_agg(temp) FROM temp'''
            cursor.execute(query,[remind_at])
            response = cursor.fetchall()
            if response and response[0] and response[0][0]:
                return response[0][0]
            return None
    
    def updateNotion(notion_id):
        with connect.cursor() as cursor:
            query = '''UPDATE Reminders
                        SET sent = %s
                        WHERE reminder_id = %s'''
            cursor.execute(query,[True, notion_id])
            return None



except Exception as _ex:
        print("[INFO][notion_operations] Error while working with PostgreSQL", _ex)