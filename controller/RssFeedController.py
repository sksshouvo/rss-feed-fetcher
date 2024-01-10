"""rss_feed_model is the base model of this application"""
from model.rss_feed_model import RssFeedModel
from classes.rss_feed import rss_feed_class
from classes.validation import Validation
from config import settings

class RssFeedController:
    """RssFeedController is the base controller of this application"""
    interval_id = None
    def __init__(self, initial_show_limit=settings.INITIAL_SHOW_LIMIT):
        """this is the constructor of this controller."""
        self.rss_feed_fetcher = rss_feed_class()
        self.rss_feed_model = RssFeedModel()
        self.rss_feed_data = []
        self.initial_show_limit = initial_show_limit
    def store(self, link_input, interval):
        """this will store rss feeds from rss feed link."""
        entry_text           = link_input.get()
        interval_value       = interval.get("value").get()
        validate_entry_text = Validation.validate_entry(entry_text)
        if not validate_entry_text:
            return validate_entry_text
        validate_interval_value = Validation.validate_interval_count(interval_value)
        if not validate_interval_value:
            return validate_interval_value
        rss_data = self.rss_feed_fetcher.fetch_rss_feed(entry_text)
        if not rss_data:
            return rss_data
        self.rss_feed_model.check_table()
        self.rss_feed_model.create(rss_data, limit=self.initial_show_limit)
        return self.all()
    def all(self):
        """This function returns all the rss feeds from database"""
        return self.rss_feed_model.get_all(limit=self.initial_show_limit)
    def show(self):
        """this wil show the stored data from rss feed link to application."""
    def delete(self):
        """this will delete data from new tables."""
    def update(self):
        """this will move data from new tables to old tables."""
    def check_new_data(self, link):
        """this checks in the database for new rss feed data."""
        return self.rss_feed_model.check_for_new_data(link)
    def __del__(self):
        """this is the destructor"""
