from connection import Connection
from datetime import date
from user_operations import *

connect = Connection().connect
try:
    # Создание новой таски
    def addNewTask(login, title, descryption = '', due_date = None, status = "open", priority = 1, parent_id = None):
        with connect.cursor() as cursor:
            user_id = getUserByLogin(login)[0]["user_id"]
            if not user_id:
                return "Error: user not exist"
            
            query = '''INSERT INTO Tasks (user_id, title, description, due_date, status, priority, creatad_at, parent_id)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
            cursor.execute(query, [user_id, title, descryption, due_date, status, priority, date.today(), parent_id])

#---------------------------------------------------------------

# Удалить таску       
    def delTask(task_id):
        with connect.cursor() as cursor:
            query = '''DELETE FROM Tasks
                        WHERE task_id = %s'''
            cursor.execute(query,[task_id])
            response = cursor.fetchall()
            return response[0][0]
    
#-----------------------Получение тасок-------------------------
    
# Получить атску по юзеру    
    def getTasksByUser(login):
        with connect.cursor() as cursor:
            user_id = getUserByLogin(login)[0]["user_id"]
            if not user_id:
                return 'Error: user not exist'
            query = '''SELECT json_agg(Tasks) FROM Tasks
                    WHERE user_id = %s
                    AND parent_id is null'''
            cursor.execute(query,[user_id])
            response = cursor.fetchall()
            return response[0][0]

# Получить сабтаску       
    def getSubTasks(task_id):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Tasks) FROM Tasks
                        WHERE parent_id = %s'''
            cursor.execute(query,[task_id])
            response = cursor.fetchall()
            return response[0][0]

 # Таска по айди       
    def getTasksById(task_id):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Tasks) FROM Tasks
                        WHERE task_id = %s'''
            cursor.execute(query,[task_id])
            response = cursor.fetchall()
            return response[0][0]

#----------------------Обновление полей тасок-----------------------

    def updateTask(task_id, title, description, due_date, status, priority, creatad_at, parent_id):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET title = %s,
                            description = %s,
                            due_date = %s,
                            status = %s,
                            priority = %s,
                            creatad_at = %s,
                            parent_id = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[title, description, due_date, status, priority, creatad_at, parent_id, task_id])
            response = cursor.fetchall()
            return None
# Обновить заголовок
    def updateTaskTitle(task_id, title):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET title = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[title, task_id])
            response = cursor.fetchall()
            return None

# Обновить описание
    def updateTaskDescription(task_id, description):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET description = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[description, task_id])
            response = cursor.fetchall()
            return None

# Обновить деделайн    
    def updateTaskDate(task_id, date):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET due_date = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[date, task_id])
            response = cursor.fetchall()
            return None

except Exception as _ex:
        print("[INFO][tasks_operations] Error while working with PostgreSQL", _ex)