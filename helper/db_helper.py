import sqlite3
import psycopg2
from config import Config


class DBHelper:

    @staticmethod
    def connect_to_db():
        return psycopg2.connect(dbname=Config.POSTGRES_DB, user=Config.POSTGRES_USER,
                                password=Config.POSTGRES_PASSWORD, host=Config.POSTGRES_HOST)

    @staticmethod
    def disconnect_from_db(conn, cursor):
        cursor.close()
        conn.close()


class DBRequest:
    _cursor = None
    _connect = None

    def __init__(self):
        self.set_connect(DBHelper.connect_to_db())
        self.set_cursor(self.get_connect().cursor())

    def set_cursor(self, cursor):
        self._cursor = cursor

    def get_cursor(self):
        return self._cursor

    def set_connect(self, connect):
        self._connect = connect

    def get_connect(self):
        return self._connect

    def complete(self):
        self.get_connect().commit()

    def close(self):
        DBHelper.disconnect_from_db(self.get_connect(), self.get_cursor())