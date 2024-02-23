"""rss_feed_model is the base model of this application"""
from model.rss_feed_model import RssFeedModel
from views.auth import LoginView
from views.view import View
import tkinter as tk


class MasterController:

    def __init__(self, model=RssFeedModel):
        self.model = model()
        self.login_view = LoginView
        self.main_view = View
        self.model.create_token_table()
        self.root = self.create_root()

    def create_root(self):
        root = tk.Tk()
        root.geometry("800x600")
        root.resizable(0, 0)
        return root

    def on_login_success(self, token):
        self.model.token = token

        if hasattr(self, 'login_view_instance'):
            self.login_view_instance.destroy_view()

        self.main_view_instance = self.main_view(
            root=self.root,
            on_logout=self.on_logout
        )
        self.main_view_instance.exe_func()

    def on_logout(self, destroy=False):
        self.model.destroy_token()

        if hasattr(self, 'main_view_instance'):
            self.main_view_instance.destroy_view()

        if destroy:
            self.root.destroy()
        else:
            self.login_view_instance = self.login_view(
                master=self.root,
                on_login_success=self.on_login_success
            )
            self.login_view_instance.exec_function()

    def exec(self):
        if not self.model.token:
            self.login_view_instance = self.login_view(
                master=self.root,
                on_login_success=self.on_login_success
            )
            self.login_view_instance.exec_function()
        else:
            self.main_view_instance = self.main_view(
                root=self.root,
                on_logout=self.on_logout
            )
            self.main_view_instance.exe_func()

    def restart_application(self):
        # Properly destroy or hide current views before restarting
        if hasattr(self, 'login_view_instance'):
            self.login_view_instance.destroy_view()
        if hasattr(self, 'main_view_instance'):
            self.main_view_instance.destroy_view()

        # Re-initialize the application
        new_master_controller = MasterController()
        new_master_controller.exec()











