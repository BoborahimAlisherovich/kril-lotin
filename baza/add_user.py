import sqlite3

def add(full_name,telegram_id):
    connection = sqlite3.connect("sqlite.db")

    command = f"""
    INSERT INTO USERS('full_name','telegram_id') 
    VALUES('{full_name}','{telegram_id}'); 

    """
    cursor = connection.cursor()

    cursor.execute(command)

    connection.commit()