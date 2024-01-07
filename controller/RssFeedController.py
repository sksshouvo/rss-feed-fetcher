from model.rss_feed_model import RssFeedModel
from classes.rss_feed import rss_feed_class
from classes.validation import Validation
from views.view import View

class RssFeedController:
    interval_id = None

    def __init__(self):
        self.init_view = View()
        self.rss_feed_fetcher = rss_feed_class()
        self.rss_feed_model = RssFeedModel()
        pass

    def index(self):
        self.init_view.exe_func()
        pass

    def store(self, entry_text, interval_value):
        # this will store rss feeds from rss feed link.
        Validation.validate_entry(entry_text)
        Validation.validate_interval_count(interval_value)
        self.rss_feed_model.check_table()
        self.rss_feed_model.create(rss_data, limit=self.initial_show_limit)
        pass

    def show(self):
        # this wil show the stored data from rss feed link to application.
        pass

    def delete(self):
        # this will delete data from new tables.
        pass

    def update(self):
        # this will move data from new tables to old tables.
        pass

    def __del__(self):
        pass
