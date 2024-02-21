'''This is the rss_feed_model file and the base model file of this application'''
import sqlite3
from config import settings
import os


class Database:
    DATABASE_PATH = settings.DATABASE_PATH
    NEW_FEEDS_TABLE = settings.NEW_TABLE_NAME
    OLD_FEEDS_TABLE = settings.OLD_TABLE_NAME
    TOKEN_TABLE = settings.TOKEN_TABLE

    def __init__(self):
        self.connection = None

    def get_connection(self):
        os.makedirs(os.path.dirname(self.DATABASE_PATH), exist_ok=True)
        if not self.connection or not self._is_connection_valid():
            self.connection = sqlite3.connect(self.DATABASE_PATH)
            return self.connection
        return self.connection

    def _is_connection_valid(self):
        if self.connection:
            try:
                self.connection.execute('SELECT 1')
                return True
            except sqlite3.Error:
                return False
        return False

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None


class RssFeedModel(Database):
    def _create_tables(self, cursor):
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.NEW_FEEDS_TABLE} (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                link TEXT NOT NULL
            )
        ''')
        return cursor

    def check_table(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(f'''SELECT name
                       FROM sqlite_master
                       WHERE type="table" AND name="{self.NEW_FEEDS_TABLE}"'''
        )
        if not cursor.fetchone():
            cursor.execute(
                f'''CREATE TABLE {self.NEW_FEEDS_TABLE} ( id INTEGER PRIMARY
                 KEY, title TEXT NOT NULL, link TEXT NOT NULL)'''
            )
            cursor.execute(
                f'''CREATE TABLE {self.OLD_FEEDS_TABLE} ( id INTEGER PRIMARY
                 KEY, title TEXT NOT NULL, link TEXT NOT NULL)'''
            )
        else:
            cursor.execute(f'''DELETE FROM {self.OLD_FEEDS_TABLE}''')
            cursor.execute(
                f'''INSERT INTO {self.OLD_FEEDS_TABLE} (id, title, link)
                 SELECT id, title, link FROM {self.NEW_FEEDS_TABLE}'''
            )
            cursor.execute(f'''DELETE FROM {self.NEW_FEEDS_TABLE}''')
        connection.commit()
        connection.close()

    def create(self, dataset, limit: int = 10):
        connection = self.get_connection()
        cursor = connection.cursor()
        self._create_tables(cursor)
        for index, data in enumerate(dataset[:limit]):
            cursor.execute(
                f'''INSERT INTO {self.NEW_FEEDS_TABLE} (title, link) VALUES (?, ?)''',
                (data.title, data.links[0].href)
            )
        connection.commit()
        connection.close()

    def get_all(self, limit=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM {self.NEW_FEEDS_TABLE} ORDER BY id ASC"
        if limit:
            query = f"{query} LIMIT 0, {limit}"
        cursor.execute(query)
        return cursor.fetchall()

    def get_single(self, condition):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM {self.NEW_FEEDS_TABLE} WHERE {condition} ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        data = cursor.fetchone()
        return data

    @staticmethod
    def update():
        pass

    @staticmethod
    def delete():
        pass

    def check_for_new_data(self, link):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(f'''SELECT *
                        FROM {self.OLD_FEEDS_TABLE} 
                        WHERE {self.OLD_FEEDS_TABLE}.link="{link}"'''
        )
        all_data = cursor.fetchone()
        connection.commit()
        connection.close()
        return all_data
    
    def create_token_table(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.TOKEN_TABLE} (
                id INTEGER PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
        return

    @property
    def token(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            f'SELECT * FROM {self.TOKEN_TABLE} ORDER BY id ASC LIMIT 1'
        )
        token = cursor.fetchone()
        connection.close()
        return token

    @token.setter
    def token(self, value):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            f'SELECT * FROM {self.TOKEN_TABLE} ORDER BY id ASC LIMIT 1'
        )
        token = cursor.fetchone()
        if token:
            cursor.execute(f'''DELETE FROM {self.TOKEN_TABLE}''')
        cursor.execute(
            f"INSERT INTO {self.TOKEN_TABLE} (value) VALUES (?)",
            (value,)
        )
        connection.commit()
        connection.close()

    def destroy_token(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(f'''DELETE FROM {self.TOKEN_TABLE}''')
        connection.commit()
        connection.close()

    