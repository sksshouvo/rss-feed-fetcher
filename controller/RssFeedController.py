from views.view import View

class RssFeedController:
    interval_id = None

    def __init__(self):
        self.init_view = View()
        pass

    def index(self):
        self.init_view.exe_func()
        pass

    def store(self):
        # this will store rss feeds from rss feed link.
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
