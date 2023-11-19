import subprocess
from plyer import notification
import config.settings as settings
from icecream import ic

class Notification:

    def __init__(self, new_data = []):
        self.new_data = new_data
        pass

    def get_notification(rss_feed_count):
        if rss_feed_count > 0:
            title = f"{settings.APP_NAME}: New Update"
            # Title and message for the notification
            message = f"{rss_feed_count} new rss feed update"
            # Sending the notification
            notification.notify(title=title, message=message, timeout=10)  # Timeout is in seconds
        pass