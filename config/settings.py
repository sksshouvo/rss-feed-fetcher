import os
from dotenv import load_dotenv

import classes.validation

load_dotenv()

APP_NAME           = os.environ.get("APP_NAME", "Rss Feed Fetcher")
FAVICON_PATH       = os.getenv("FAVICON_PATH", "./assets/images/favicon.png")
DATABASE_PATH      = os.environ.get("DATABASE_PATH", "databases/rss_feed.db")
NEW_TABLE_NAME     = os.environ.get("NEW_TABLE_NAME", "new_rss_feeds")
OLD_TABLE_NAME     = os.environ.get("OLD_TABLE_NAME", "old_rss_feeds")
TOKEN_TABLE        = os.environ.get("TOKEN_TABLE", "tokens")
INITIAL_SHOW_LIMIT = int(os.environ.get("INITIAL_SHOW_LIMIT", 10))
NOTIFICATION_SOUND_PATH = os.environ.get("NOTIFICATION_SOUND_PATH", "assets/sounds/default_notifications.mp3")


AUTH_PASSWORD_VALIDATORS = [
    classes.validation.CommonPasswordValidator,
    classes.validation.MinimumLengthValidator,
    classes.validation.NumericPasswordValidator
]

API_BASE_URI = os.environ.get("API_BASE_URI", "http://127.0.0.1:8000/api/")
