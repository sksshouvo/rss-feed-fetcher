import webbrowser

import tkinter
import tkinter.font as tkFont
from tkinter import messagebox

from classes.rss_feed import rss_feed_class
from classes.validation import Validation
from config import settings
from model.rss_feed_model import RssFeedModel
from classes.notifier.test_notifications import LinuxNotificationHandler
from classes.notifications import NotificationHandler
import threading


class View:
    interval_id = None

    def __init__(
        self,
        app_name=settings.APP_NAME,
        favicon_path=settings.FAVICON_PATH,
        initial_show_limit=settings.INITIAL_SHOW_LIMIT
    ):
        self.favicon_path = favicon_path
        self.app_name = app_name
        self.initial_show_limit = initial_show_limit
        self.root = tkinter.Tk()
        self.rss_feed_data = []
        self.listbox = ""

    @staticmethod
    def on_validate_input(P):
        # This function is called when the Entry widget is modified
        # Check if the input is a valid number with a maximum length of 2
        return P.isdigit() and len(P) <= 2

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)
            link = self.rss_feed_data[selected_index[0]][2]  # Assuming 'link' is in the third column
            confirmation = messagebox.askyesno("Confirmation", f"Do you want to open the link:\n{link}?")
            if confirmation:
                # Open the link in the default web browser
                webbrowser.open_new_tab(link)

    def on_start_button_click(self, link_input, interval):
        self.start_button.config(text="Running", state="disabled")
        self.stop_button.config(text="Stop", state="normal")

        self.start_action(link_input, interval)

    def start_action(self, link_input, interval):
        rss_feed_fetcher = rss_feed_class()
        rss_feed_model = RssFeedModel()
        entry_text = link_input.get()
        interval_value = interval.get("value").get()
        interval_unit = interval.get("unit").get()

        try:
            # Attempt to validate the entry
            Validation.validate_entry(entry_text)
            Validation.validate_interval_count(interval_value)
            rss_data = rss_feed_fetcher.fetch_rss_feed(entry_text)
            rss_feed_model.check_table()
            rss_feed_model.create(rss_data, limit=self.initial_show_limit)

            self.rss_feed_data = rss_feed_model.get_all(limit=self.initial_show_limit)

            self.listbox = tkinter.Listbox()
            self.listbox.place(x=20, y=190, width=750)
            new_rss_feeds = []
            old_rss_feeds = []
            # new_rss_feed_count = 0
            for index, feed_data in enumerate(self.rss_feed_data[:self.initial_show_limit], start=1):
                data_set = f"{index}\t -\t {feed_data[1]}"
                if not rss_feed_model.check_for_new_data(link=feed_data[2]):
                    data_set += "  ( NEW )"
                    new_rss_feeds.append(data_set)
                    new_rss_feed_count = 1 + index
                else:
                    old_rss_feeds.append(data_set)

            full_data_set = new_rss_feeds + old_rss_feeds

            for data in full_data_set:
                self.listbox.insert(tkinter.END, data)

            notification_handler = NotificationHandler(self.root)
            notification_handler.handle_notifications(new_rss_feeds)
            # threading.Thread(target=notification_handler.handle_notifications, args=[new_rss_feeds])

            # lnh = LinuxNotificationHandler()
            # lnh.show_notification("Title", "NEw message")

            # Notification.get_notification(new_rss_feed_count)

            new_rss_feed_count = 0
            self.listbox.bind("<<ListboxSelect>>", self.on_select)
            self.schedule_refresh(link_input, interval)
        except ValueError as e:
            # Display an error message when validation fails
            messagebox.showerror("Error", str(e))

    def schedule_refresh(self, link_input, interval: dict):
        # Get the interval value and unit
        interval_value = int(interval.get("value").get())
        interval_unit = interval.get("unit").get()

        # Calculate interval in milliseconds based on the selected unit
        interval_ms = self.calculate_interval_milliseconds(interval_value, interval_unit)

        # Schedule the refresh after the specified interval
        self.interval_id = self.root.after(interval_ms, lambda: self.start_action(link_input, interval))

    @staticmethod
    def calculate_interval_milliseconds(interval_count, interval_unit):
        # value = interval_count_input.get()
        # unit = interval_unit_input.get()

        interval_mapping = {
            "SEC": 1000,  # Convert seconds to milliseconds
            "MIN": 60 * 1000,  # Convert minutes to milliseconds
            "HOUR": 60 * 60 * 1000,  # Convert hours to milliseconds
            "DAYS": 24 * 60 * 60 * 1000,  # Convert days to milliseconds
            "MONTH": 30 * 24 * 60 * 60 * 1000  # Approximate month to milliseconds (adjust as needed)
        }
        return interval_count * interval_mapping[interval_unit]

    def stop_action(self):
        if self.interval_id:
            self.root.after_cancel(self.interval_id)
            self.interval_id = None  # Reset the interval ID

    def on_stop_button_click(self):
        # Call the stop_action method when the "Stop" button is clicked
        self.stop_action()
        self.start_button.config(text="Start", state="normal")
        self.stop_button.config(text="Stopped", state="disabled")

    def exe_func(self):

        img = tkinter.PhotoImage(file=self.favicon_path)

        fontObj = tkFont.Font(size=15)
        self.root.iconphoto(False, img)
        self.root.title(self.app_name)
        self.root.geometry("800x600")
        # Create a LabelFrame
        frame = tkinter.Frame(
            self.root,
            width=775,
            height=100,
            bg="white",
            highlightbackground="black",
            highlightthickness=2,
            borderwidth=2
        )
        # Configure the Frame
        frame.place(x=10, y=20)
        # link entry field
        link_input = tkinter.Entry(
            self.root,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        link_input.insert(0, "  Paste Your Rss Feed Link Here...")
        link_input.place(x=20, y=40, width=750, height=30)
        self.root.resizable(0, 0)
        # text field
        text_label = tkinter.Label(self.root, text="Refresh in every", bg='white')
        text_label.place(x=20, y=80)
        # interval count field
        interval_count_input = tkinter.Entry(
            self.root,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        interval_count_input.place(x=120, y=80, width=35)
        validate_input = self.root.register(self.on_validate_input)
        interval_count_input.config(
            validate="key",
            validatecommand=(validate_input, "%P")
        )

        # Dropdown menu options
        options = [
            "SEC",
            "MIN",
            "HOUR",
            "DAYS",
            "MONTH"
        ]

        # datatype of menu text
        clicked = tkinter.StringVar()

        # initial menu text
        clicked.set("MIN")

        # Create Dropdown menu
        interval = tkinter.OptionMenu(self.root, clicked, *options)
        interval.place(x=160, y=75)

        interval_period = dict(
            value=interval_count_input,
            unit=clicked,
        )

        # start button
        start_button = tkinter.Button(
            self.root,
            text="Start",
            command=lambda link=link_input, interval_period=interval_period: self.on_start_button_click(link, interval_period)
        )
        start_button.place(x=625, y=75, width=70, height=30)

        self.start_button = start_button

        # start button
        stop_button = tkinter.Button(
            self.root,
            text="Stop",
            command=self.on_stop_button_click
        )
        stop_button.place(x=700, y=75, width=70, height=30)
        self.stop_button = stop_button
        # Code to add widgets will go here...
        # Create a LabelFrame
        data_section_frame = tkinter.Frame(
            self.root,
            width=775,
            height=420,
            bg="white",
            highlightbackground="black",
            highlightthickness=2,
            borderwidth=2
        )
        # Configure the Frame
        data_section_frame.place(x=10, y=150)
        # text field
        rss_feed_text = tkinter.Label(self.root, text="Rss Feed List", bg='white', font=fontObj)
        rss_feed_text.place(x=20, y=160)
        self.root.mainloop()
