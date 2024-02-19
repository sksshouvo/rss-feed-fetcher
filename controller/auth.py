"""rss_feed_model is the base model of this application"""
from model.rss_feed_model import RssFeedModel
from views.auth import LoginView
from views.view import View


class MasterController:

    def __init__(self, model=RssFeedModel):
        self.model = model()
        self.login_view = LoginView
        self.main_view = View
        self.model.create_token_table()

    def exec(self):
        def on_login_success(response):
            token = response
            self.model.token = token.get('access_token')

        while not self.model.token:
            login_view = self.login_view(
                controller=self,
                on_login_success=on_login_success
            )
            login_view.master.mainloop()

        main_view = self.main_view()
        main_view.exe_func()










