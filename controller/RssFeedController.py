from model.rss_feed_model import RssFeedModel
from classes.rss_feed import rss_feed_class
from classes.validation import Validation
from views.view import View

class RssFeedController:
    interval_id = None

    def __init__(self, initial_show_limit=settings.INITIAL_SHOW_LIMIT):
        self.init_view = View()
        self.rss_feed_fetcher = rss_feed_class()
        self.rss_feed_model = RssFeedModel()
        self.rss_feed_data = []
        self.initial_show_limit = initial_show_limit
        pass

    def index(self):
        self.init_view.exe_func()
        pass

    def store(self, link_input, interval):
        # this will store rss feeds from rss feed link.
        entry_text           = link_input.get()
        interval_value       = interval.get("value").get()
        validate_entry_text = Validation.validate_entry(entry_text)
        if not validate_entry_text:
                return validate_entry_text;
        else:
            validate_interval_value = Validation.validate_interval_count(interval_value)
            if not validate_interval_value:
                return validate_interval_value
            else:
                rss_data = self.rss_feed_fetcher.fetch_rss_feed(entry_text)
                self.rss_feed_model.check_table()
                self.rss_feed_model.create(rss_data, limit=self.initial_show_limit)
                self.rss_feed_data = self.all()

                return self.rss_feed_data
    pass

    def all(self):
        self.rss_feed_data = self.rss_feed_model.get_all(limit=self.initial_show_limit)
        return self.rss_feed_data
    def show(self):
        # this wil show the stored data from rss feed link to application.
        pass

    def delete(self):
        # this will delete data from new tables.
        pass

    def update(self):
        # this will move data from new tables to old tables.
        pass
    def check_new_data(self, link):
        self.rss_feed_data = self.rss_feed_model.check_for_new_data(link=feed_data[2])
        return self.rss_feed_data
    def __del__(self):
        pass
