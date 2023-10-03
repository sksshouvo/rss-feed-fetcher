import json
import sqlite3
from tkinter import messagebox
from classes.validation import Validation

class rss_feed_class:
    def __init__(self):
        pass

    @staticmethod
    def fetch_rss_feed(rss_feed_link):
        rss_feed_link_validation = Validation.rss_feed_link_validation(rss_feed_link)
        print('Number of posts in RSS feed :', len(rss_feed_link_validation))
        print(json.dumps(rss_feed_link_validation, indent=4))
        return json.dumps(rss_feed_link_validation)
    pass

    @staticmethod
    def store_rss_feed(rss_feed_data):
        try:
            sqlite3.connect('databases/rss_feed.db')
            print("Opened database successfully")
        except ValueError as e:
            # Display an error message when validation fails
            messagebox.showerror("Error", str(e))
        pass
