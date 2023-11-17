import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.environ.get("DATABASE_PATH", "databases/rss_feed.db")
NEW_TABLE_NAME = os.environ.get("NEW_TABLE_NAME", "new_rss_feeds")
OLD_TABLE_NAME = os.environ.get("OLD_TABLE_NAME", "old_rss_feeds")
