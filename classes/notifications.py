import subprocess
from plyer import notification
import config.settings as settings
from icecream import ic
import sys
import os
import time
from playsound import playsound
from plyer import notification
from classes.notifier.test_notifications import LinuxNotificationHandler
import threading


class NotificationHandler:
    driver = LinuxNotificationHandler
    notification_sound = settings.NOTIFICATION_SOUND_PATH
    icon = settings.FAVICON_PATH

    def __init__(self, app_window):
        self.app_window = app_window

    def get_driver(self):
        if sys.platform.startswith('linux'):
            return LinuxNotificationHandler
        else:
            raise OSError('Please develop a Notification Handler like ( LinuxNotificationHandler ) in classes.notifier')

    def make_notification(self, new_data):
        count = 0
        if new_data:
            count = len(new_data)

        notification_details = dict(
            title=f"Refreshed Feed : {count} new posts found!",
            message='\n'.join(new_data),
            app_name=settings.APP_NAME,
            timeout=10,
            icon=self.icon,
        )
        return notification_details

    def show_notification(self, new_data):
        driver = self.get_driver()
        handler = driver()

        notification_details = self.make_notification(new_data)

        handler.show_notification(notification_details)

        notification_details = self.make_notification(new_data)

        # driver.notify(**notification_details)

        playsound(self.notification_sound)

    def handle_notifications(self, new_data):
        self.show_notification(new_data)
        notification_thread = threading.Thread(target=self.show_notification, args=(new_data,))
        notification_thread.start()
        # notification.on_click(self.open_app_window)

    # def open_app_window(self, *args):
    #     self.app_window.deiconify()
