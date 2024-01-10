import json
import sqlite3
from tkinter import messagebox
from classes.validation import Validation

class rss_feed_class:
    def __init__(self):
        pass
    @staticmethod
    def fetch_rss_feed(rss_feed_link):
        return Validation.rss_feed_link_validation(rss_feed_link)
    @staticmethod
    def store_rss_feed(rss_feed_data):
        try:
            sqlite3.connect('databases/rss_feed.db')
        except ValueError as e:
            # Display an error message when validation fails
            messagebox.showerror("Error", str(e))
