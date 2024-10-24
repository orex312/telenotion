import psycopg2
from config import host, user, password, db_name
from create_tables import create_tables

def malke_connection():
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name    
        )
        connection.autocommit = True
        
        create_tables(connection)   

        return connection
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            # cursor.close()
            connection.close()
            print("[INFO] PostgreSQL connection closed")