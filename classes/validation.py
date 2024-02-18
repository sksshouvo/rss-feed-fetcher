from tkinter import messagebox
import feedparser
import gzip
from abc import ABC, abstractmethod
from pathlib import Path


class Validator(ABC):
    @abstractmethod
    def validate(self, value, messagebox):
        pass


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


class MinimumLengthValidator(Validator):
    """
    Validate that the password is of a minimum length.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, messagebox):
        if len(password) < self.min_length:
            messagebox.showerror(
                'Invalid Password Length',
                'Password must be at least 8 characters long, '
            )
            return False
        return True


class CommonPasswordValidator(Validator):
    """
    Validate that the password is not a common password.
    """

    @property
    def DEFAULT_PASSWORD_LIST_PATH(self):
        # return "assets/common-passwords.txt.gz"
        return Path(__file__).resolve().parent.parent / \
            "assets/common-passwords.txt.gz"

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        if password_list_path is CommonPasswordValidator.DEFAULT_PASSWORD_LIST_PATH:
            password_list_path = self.DEFAULT_PASSWORD_LIST_PATH
        try:
            with gzip.open(password_list_path, "rt", encoding="utf-8") as f:
                self.passwords = {x.strip() for x in f}
        except OSError:
            with open(password_list_path) as f:
                self.passwords = {x.strip() for x in f}

    def validate(self, password, messagebox):
        if password.lower().strip() in self.passwords:
            messagebox.showerror(
                'Common Password',
                'This password is too common.'
            )
            return False
        return True


class NumericPasswordValidator(Validator):
    """
    Validate that the password is not entirely numeric.
    """

    def validate(self, password, messagebox):
        if password.isdigit():
            messagebox.showerror(
                'Only Numbers',
                'This password is entirely numeric.'
            )
            return False
        return True
