import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.environ.get("APP_NAME", "Rss Feed Fetcher")
FAVICON_PATH = os.getenv("FAVICON_PATH", "./assets/images/favicon.png")


DATABASE_PATH = os.environ.get("DATABASE_PATH", "databases/rss_feed.db")
NEW_TABLE_NAME = os.environ.get("NEW_TABLE_NAME", "new_rss_feeds")
OLD_TABLE_NAME = os.environ.get("OLD_TABLE_NAME", "old_rss_feeds")
INITIAL_SHOW_LIMIT = int(os.environ.get("INITIAL_SHOW_LIMIT", 10))
