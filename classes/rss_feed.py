import json
import feedparser
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
