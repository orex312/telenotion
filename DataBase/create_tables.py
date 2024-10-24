import psycopg2
import json
from config import host, user, password, db_name



def create_tables(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS Users (
                    "user_id" int NOT NULL,
                    "user_name" varchar(50) NOT NULL,
                    "login" varchar(50) NOT NULL,
                    "creatad_at" date NOT NULL DEFAULT '1.1.2000',
                    "timezone" int NOT NULL DEFAULT 3,
                    PRIMARY KEY (user_id)
                );

                CREATE TABLE IF NOT EXISTS Tasks(
                    "task_id" int NOT NULL,
                    "user_id" int NOT NULL,
                    "title" varchar(50) NOT NULL,
                    "description" varchar(250),
                    "due_date" date,
                    "status" varchar(20),
                    "priority" varchar(250),
                    "creatad_at" date NOT NULL DEFAULT '1.1.2000',
                    "parent_id" int REFERENCES Tasks(task_id),
                    PRIMARY KEY(task_id),
                    FOREIGN KEY(user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY(parent_id) REFERENCES Tasks(task_id)
                );

                CREATE TABLE IF NOT EXISTS Reminders (
                    "reminder_id" int NOT NULL,
                    "task_id" int NOT NULL,
                    "remind_at" timestamp NOT NULL,
                    "sent" bool DEFAULT False,
                    PRIMARY KEY (reminder_id),
                    FOREIGN KEY(task_id) REFERENCES Tasks(task_id) ON DELETE CASCADE
                );'''
        )
