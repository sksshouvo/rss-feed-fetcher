import sqlite3

class rss_feed_models:
    def __init__(self):
        pass

    @staticmethod
    def check_table():
        connection = sqlite3.connect('databases/rss_feed.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='new_rss_feeds'")

        if not cursor.fetchone():
            print("checking shit")
            cursor.execute('''CREATE TABLE new_rss_feeds ( id INTEGER PRIMARY KEY, title TEXT NOT NULL, link TEXT NOT NULL)''')
            print("new_rss_feeds table created")
            cursor.execute('''CREATE TABLE old_rss_feeds ( id INTEGER PRIMARY KEY, title TEXT NOT NULL, link TEXT NOT NULL)''')
            print("old_rss_feeds table created")
        else:
            cursor.execute('''DELETE FROM old_rss_feeds''')
            print("old_rss_feeds table deleted")
            cursor.execute('''INSERT INTO old_rss_feeds (id, title, link) SELECT id, title, link FROM new_rss_feeds''')
            print("old_rss_feeds table inserted")
            cursor.execute('''DELETE FROM new_rss_feeds''')
            print("new_rss_feeds table deleted")
        connection.commit()
        connection.close()
    @staticmethod
    def get_all():
        pass

    @staticmethod
    def get_10_rows():
        connection = sqlite3.connect('databases/rss_feed.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM new_rss_feeds LIMIT 0,10")
        data = cursor.fetchall()
        print("fetched 10 datas from new_rss_feeds")
        return data


    @staticmethod
    def get_single():
        pass
    
    @staticmethod
    def create(datas):
        connection = sqlite3.connect('databases/rss_feed.db')
        cursor = connection.cursor()
        count = 0
        if len(datas):
            for data in datas:
                cursor.execute('''INSERT INTO new_rss_feeds (title, link) VALUES (?, ?)''', (data.title, data.links[0].href))
                count += 1
                if count == 10:
                    break
        connection.commit()
        connection.close()
        print("data successfully inserted")

    @staticmethod
    def update():
        pass

    @staticmethod
    def delete():
        pass

