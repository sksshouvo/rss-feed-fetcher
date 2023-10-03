import os
import tkinter
from dotenv import load_dotenv
from tkinter import messagebox
from classes.rss_feed import rss_feed_class
from classes.validation import Validation
import tkinter.font as tkFont

load_dotenv()


class View:
    def __init__(
        self, app_name=os.getenv("APP_NAME"),
        favicon_path=os.getenv("FAVICON_PATH")
    ):
        self.favicon_path = favicon_path
        self.app_name = app_name

    @staticmethod
    def on_validate_input(P):
        # This function is called when the Entry widget is modified
        # Check if the input is a valid number with a maximum length of 2
        return P.isdigit() and len(P) <= 2

    @staticmethod
    def start_action(link_input, interval_count):
        rss_feed_fetcher = rss_feed_class()
        entry_text = link_input.get()
        entry_number = interval_count.get()

        try:
            # Attempt to validate the entry
            Validation.validate_entry(entry_text)
            Validation.validate_interval_count(entry_number)
            rss_data = rss_feed_fetcher.fetch_rss_feed(entry_text)
            rss_feed_fetcher.store_rss_feed(rss_data)
        except ValueError as e:
            # Display an error message when validation fails
            messagebox.showerror("Error", str(e))
            
    def exe_func(self):
        root = tkinter.Tk()
        img  = tkinter.PhotoImage(file=self.favicon_path)
        
        #creating a font object
        fontObj = tkFont.Font(size=15)
        root.iconphoto(False, img)
        root.title(self.app_name)
        root.geometry("800x600")
        # Create a LabelFrame
        frame = tkinter.Frame(
            root,
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
            root,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        link_input.insert(0, "  Paste Your Rss Feed Link Here...")
        link_input.place(x=20, y=40, width=750, height=30)
        root.resizable(0, 0)
        # text field
        text_label = tkinter.Label(root, text="Refresh in every", bg='white')
        text_label.place(x=20, y=80)
        # interval count field
        interval_count_input = tkinter.Entry(
            root,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        interval_count_input.place(x=120, y=80, width=35)
        validate_input = root.register(self.on_validate_input)
        interval_count_input.config(
            validate="key",
            validatecommand=(validate_input, "%P")
        )

        # Dropdown menu options
        options = [
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
        interval = tkinter.OptionMenu(root, clicked, *options)
        interval.place(x=160, y=75)
        # start button
        start_button = tkinter.Button(
            root,
            text="Start",
             command=lambda entry=link_input, interval_count = interval_count_input : self.start_action(entry, interval_count)
        )
        start_button.place(x=625, y=75, width=70, height=30)
        # start button
        stop_button = tkinter.Button(root, text="Stop")
        stop_button.place(x=700, y=75, width=70, height=30)
        # Code to add widgets will go here...
        # Create a LabelFrame
        data_section_frame = tkinter.Frame(
            root,
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
        rss_feed_text = tkinter.Label(root, text="Rss Feed List", bg='white', font=fontObj)
        rss_feed_text.place(x=20, y=160)
        root.mainloop()
