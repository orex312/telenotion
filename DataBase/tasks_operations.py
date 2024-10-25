from connection import Connection
from datetime import date

connect = Connection().connect
try:
    def addNewTask(login, title, descryption = '', due_date = date.today(), status = "open", priority = 1, parent_id = None):
        with connect.cursor() as cursor:
            query = '''SELECT user_id FROM Users
                    WHERE login = %s'''
            cursor.execute(query,[login])
            user_id = cursor.fetchall()[0]
            if not user_id:
                return "user not exist"
            
            query = '''INSERT INTO Tasks (user_id, title, description, due_date, status, priority, creatad_at, parent_id)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
            cursor.execute(query, [user_id, title, descryption, due_date, status, priority, date.today(), parent_id])

    def getTasksByUser(login):
        with connect.cursor() as cursor:
            query = '''SELECT user_id FROM Users
                    WHERE login = %s'''
            cursor.execute(query,[login])
            user_id = cursor.fetchall()[0]
            query = '''SELECT json_agg(Tasks) FROM Tasks
                    WHERE user_id = %s
                    AND parent_id is null'''
            cursor.execute(query,[user_id])
            response = cursor.fetchall()
            return response[0][0]
        
    def getSubTasks(task_id):
        with connect.cursor() as cursor:
            query = '''SELECT json_agg(Tasks) FROM Tasks
                        WHERE parent_id = %s'''
            cursor.execute(query,[task_id])
            response = cursor.fetchall()
            return response[0][0]
        
    def delTask(task_id):
        with connect.cursor() as cursor:
            query = '''DELETE FROM Tasks
                        WHERE task_id = %s'''
            cursor.execute(query,[task_id])
            response = cursor.fetchall()
            return response[0][0]

except Exception as _ex:
        print("[INFO][tasks_operations] Error while working with PostgreSQL", _ex)