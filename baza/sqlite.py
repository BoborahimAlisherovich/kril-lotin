import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS USERS(
        id INTEGER PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        phone_number VARCHAR(13),
        telegram_id NUMBER unique );
              """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())


    async def add_user(self, telegram_id:int, first_name:str,last_name:str,phone_number:str):
        sql = """
        INSERT INTO Users(first_name,last_name,phone_number,telegram_id) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(first_name,last_name,phone_number,telegram_id), commit=True)

    async def update_user(self, telegram_id:int, first_name:str,last_name:str,phone_number:str):
        sql = """
        UPDATE Users
        SET first_name = ?, last_name = ?, phone_number = ?
        WHERE telegram_id = ?;
        """
        self.execute(sql, parameters=(first_name,last_name,phone_number,telegram_id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)


    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)


    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)
    
    async def all_users_id(self):
        return self.execute("SELECT telegram_id FROM Users;", fetchall=True)
    


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")