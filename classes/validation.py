from tkinter import messagebox
import feedparser

class Validation:

    @staticmethod
    def validate_entry(entry_text):
        if not entry_text.strip():
            messagebox.showwarning("Warning", "Link field cannot be empty.")
            return False
        return True
    
    @staticmethod
    def validate_interval_count(entry_number):
        if not entry_number.strip():
            messagebox.showwarning("Warning", "Interval Count is invalid.")
            return False
        return True
    
    @staticmethod
    def rss_feed_link_validation(rss_feed_link):
        feed = feedparser.parse(rss_feed_link)
        if not len(feed.entries): 
            messagebox.showwarning("Warning", "Invalid rss feed Link")
            return False
        return feed.entries