import sqlite3

def allusers():
    connection = sqlite3.connect("sqlite.db")

    command = """
    SELECT count(*) from USERS;
    """

    cursor = connection.cursor()

    cursor.execute(command)

    users = cursor.fetchone()

    return users


def allusers_id():
    connection = sqlite3.connect("sqlite.db")

    command = """
    SELECT telegram_id from USERS;
    """

    cursor = connection.cursor()

    cursor.execute(command)

    users = cursor.fetchall()

    return users