from connection import Connection
from datetime import date
from user_operations import *

connect = Connection().connect
try:
    # Создание новой таски
    def addNewTask(user_id, title, description = '', due_date = None, status = "open", priority = 1, parent_id = None):
        with connect.cursor() as cursor:
            query = '''select max(task_id) from tasks'''
            cursor.execute(query)
            task_id = cursor.fetchall()[0][0]
            print(task_id)
            if task_id == None:
                task_id = 1
            else:
                task_id += 1
            query = '''INSERT INTO Tasks (task_id, user_id, title, description, due_date, status, priority, creatad_at, parent_id)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            cursor.execute(query, [task_id, user_id, title, description, due_date, status, priority,\
                                   datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), parent_id])
            return task_id

#---------------------------------------------------------------

# Удалить таску       
    def delTask(task_id):
        with connect.cursor() as cursor:
            query = '''DELETE FROM Tasks
                        WHERE task_id = %s'''
            cursor.execute(query,[task_id])
            return 0
    
#-----------------------Получение тасок-------------------------
    
# Получить атску по юзеру    
    def getTasksByUser(user_id):
        with connect.cursor() as cursor:
            query = '''with temp as(
                            SELECT * FROM Tasks
                                WHERE user_id = %s
                                AND parent_id is null
                                order by creatad_at desc)
                        select jsonb_agg(temp) from temp '''
            cursor.execute(query,[user_id])
            response = cursor.fetchone()
            return response[0]

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
            return None
# Обновить заголовок
    def updateTaskTitle(task_id, title):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET title = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[title, task_id])
            return None

# Обновить описание
    def updateTaskDescription(task_id, description):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET description = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[description, task_id])
            return None

# Обновить деделайн    
    def updateTaskDate(task_id, date):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET due_date = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[date, task_id])
            return None
        
# Обновить статус   
    def updateTaskStatus(task_id, status):
        with connect.cursor() as cursor:
            query = '''UPDATE Tasks
                        SET status = %s
                        WHERE task_id = %s'''
            cursor.execute(query,[status, task_id])
            return None

except Exception as _ex:
        print("[INFO][tasks_operations] Error while working with PostgreSQL", _ex)