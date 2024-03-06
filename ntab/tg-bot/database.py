import psycopg2
from config import auth_db


class UserDB:
    def __init__(self):
        self.__conn = psycopg2.connect(auth_db)
        self.__cursor = self.__conn.cursor()
        self.__conn.autocommit = True
        self.__create_table()

    def __enter__(self):
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__conn.close()

    def __create_table(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS users "
                              "(id SERIAL PRIMARY KEY,"
                              "tg_id_user INTEGER,"
                              "tg_sources TEXT ARRAY,"
                              "web_sources TEXT ARRAY)")

    def add_user(self, tg_id_user, tg_sources, web_sources):
        if self.get_sources(tg_id_user):
            return
        self.__cursor.execute(f"INSERT INTO users (tg_id_user, tg_sources, web_sources) "
                              f"VALUES (%s, %s, %s);", (tg_id_user, tg_sources, web_sources,))

    def delete_user(self, tg_id_user):
        self.__cursor.execute(f"DELETE FROM users "
                              f"WHERE tg_id_user = '{tg_id_user}'")
        
    def get_users_id(self):
        self.__cursor.execute(f"SELECT tg_id_user FROM users")
        return self.__cursor.fetchall()


    def get_sources(self, tg_id_user):
        self.__cursor.execute(f"SELECT tg_sources FROM users WHERE tg_id_user = '{tg_id_user}';")
        data = self.__cursor.fetchone()
        return data[0] if not data is None else None

    def update_tg_sources_user(self, name_user, tg_sources):
        self.__cursor.execute(f"UPDATE users "
                              f"SET tg_sources = tg_sources || (%s)"
                              f"WHERE tg_id_user = (%s)", (tg_sources, name_user,))

    def update_web_sources_user(self, tg_id_user, web_sources):
        self.__cursor.execute(f"UPDATE users "
                              f"SET web_sources = web_sources || (%s)"
                              f"WHERE tg_id_user = (%s)", (web_sources, tg_id_user,))
