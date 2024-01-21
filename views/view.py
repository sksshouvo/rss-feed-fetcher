from controller.RssFeedController import RssFeedController
from classes.notification import Notification_Manager
from playsound import playsound
from tkinter import messagebox
import tkinter.font as tkFont
from functools import partial
from config import settings
import webbrowser
import tkinter
import requests


class View:
    interval_id = None

    def __init__(
            self,
            app_name=settings.APP_NAME,
            favicon_path=settings.FAVICON_PATH,
            initial_show_limit=settings.INITIAL_SHOW_LIMIT,
            api_base_uri=settings.BASE_API_URI
    ):
        self.favicon_path = favicon_path
        self.app_name = app_name
        self.initial_show_limit = initial_show_limit
        self.api_base_uri = api_base_uri
        self.root = tkinter.Tk()
        self.rss_feed_data = []
        self.listbox = ""
        self.notification_manager = Notification_Manager(background="white")
        self.new_rss_feed_count = 0
        self.sound_file_path = "./assets/sounds/notification_sound.wav"
        self.rss_feed_controller = RssFeedController()

    @staticmethod
    def on_validate_input(P):
        # This function is called when the Entry widget is modified
        # Check if the input is a valid number with a maximum length of 2
        return P.isdigit() and len(P) <= 2

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            link = self.rss_feed_data[selected_index[0]][
                2]  # Assuming 'link' is in the third column
            confirmation = messagebox.askyesno(
                "Confirmation",
                f"Do you want to open the link:\n{link}?"
            )
            if confirmation:
                # Open the link in the default web browser
                webbrowser.open_new_tab(link)

    def on_start_button_click(self, link_input, interval):
        check_engine = self.start_action(link_input, interval)
        if not check_engine:
            return False
        else:
            self.start_button.config(text="Running", state="disabled")
            self.stop_button.config(text="Stop", state="normal")
            return True

    def start_action(self, link_input, interval):
        new_rss_feeds = []
        old_rss_feeds = []
        self.new_rss_feed_count = 0
        self.rss_feed_data = self.rss_feed_controller.store(link_input,
                                                            interval)
        if not self.rss_feed_data:
            return self.rss_feed_data
        else:
            self.listbox = tkinter.Listbox()
            self.listbox.place(x=20, y=190, width=750)

            for index, feed_data in enumerate(
                    self.rss_feed_data[:self.initial_show_limit], start=1):
                data_set = f"{index}\t -\t {feed_data[1]}"
                if not self.rss_feed_controller.check_new_data(
                        link=feed_data[2]):
                    data_set += "  ( NEW )"
                    new_rss_feeds.append(data_set)
                    self.new_rss_feed_count += 1
                else:
                    old_rss_feeds.append(data_set)

            full_data_set = new_rss_feeds + old_rss_feeds

            for data in full_data_set:
                self.listbox.insert(tkinter.END, data)

            if (self.new_rss_feed_count):
                notification_text = f"New Notification!\
                n{self.new_rss_feed_count} new updates"
                self.notification_manager.info(notification_text, font=None,
                                               width=20)
                playsound(self.sound_file_path)

            self.listbox.bind("<<ListboxSelect>>", self.on_select)
            self.schedule_refresh(link_input, interval)
            return True

    def schedule_refresh(self, link_input, interval: dict):
        # Get the interval value and unit
        interval_value = int(interval.get("value").get())
        interval_unit = interval.get("unit").get()

        # Calculate interval in milliseconds based on the selected unit
        interval_ms = self.calculate_interval_milliseconds(interval_value,
                                                           interval_unit)

        # Schedule the refresh after the specified interval
        self.interval_id = self.root.after(
            interval_ms,
            partial(self.start_action, link_input, interval)
        )

    @staticmethod
    def calculate_interval_milliseconds(interval_count, interval_unit):
        # value = interval_count_input.get()
        # unit = interval_unit_input.get()
        interval_mapping = {
            "MIN": 60 * 1000,  # Convert minutes to milliseconds
            "HOUR": 60 * 60 * 1000,  # Convert hours to milliseconds
            "DAYS": 24 * 60 * 60 * 1000,  # Convert days to milliseconds
            "MONTH": 30 * 24 * 60 * 60 * 1000
            # Approximate month to milliseconds (adjust as needed)
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

    def signup_user(self, first_name, last_name, email, password):
        signup_url = f'{self.api_base_uri}/register/'
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }

        try:
            response = requests.post(signup_url, json=data)
            response.raise_for_status()
            result = response.json()['data']
            setattr(self, 'authorization', f'Bearer '
                                           f'{result.get("access_token")}')
            print("Signup successful:", result)
            return result
        except requests.exceptions.RequestException as ex:
            print("Signup failed:", ex)
            return None

    def on_signup_button_click(
            self,
            signup_frame,
            first_name_entry,
            last_name_entry,
            email_entry,
            password_entry
    ):
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        signed_up = self.signup_user(first_name, last_name, email, password)

        if signed_up:
            # Close the signup window
            self.root.focus_set()
            self.root.grab_set()
            self.root.grab_release()
            signup_frame.destroy()
        else:
            # Display an error message in the same frame
            error_label = tkinter.Label(
                signup_frame,
                text="Error signing up. Please try again.",
                bg='white',
                fg='red'
            )
            error_label.grid(row=5, column=0, columnspan=2, pady=10)

    def create_signup_page(self):
        signup_frame = tkinter.Frame(
            self.root,
            width=300,
            height=250,
            bg="white",
            highlightbackground="black",
            highlightthickness=2
        )
        signup_frame.place(x=250, y=200)

        first_name_label = tkinter.Label(
            signup_frame,
            text="First Name:",
            bg='white'
        )
        first_name_label.grid(row=0, column=0, padx=10, pady=10)
        first_name_entry = tkinter.Entry(
            signup_frame,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        first_name_entry.grid(row=0, column=1, padx=10, pady=10)

        last_name_label = tkinter.Label(
            signup_frame,
            text="Last Name:",
            bg='white'
        )
        last_name_label.grid(row=1, column=0, padx=10, pady=10)
        last_name_entry = tkinter.Entry(
            signup_frame,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        last_name_entry.grid(row=1, column=1, padx=10, pady=10)

        email_label = tkinter.Label(signup_frame, text="Email:", bg='white')
        email_label.grid(row=2, column=0, padx=10, pady=10)
        email_entry = tkinter.Entry(
            signup_frame,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        password_label = tkinter.Label(
            signup_frame,
            text="Password:",
            bg='white'
        )
        password_label.grid(row=3, column=0, padx=10, pady=10)
        password_entry = tkinter.Entry(
            signup_frame,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1,
            show="*"
        )
        password_entry.grid(row=3, column=1, padx=10, pady=10)

        signup_button = tkinter.Button(
            signup_frame,
            text="Signup",
            command=lambda s=signup_frame,
                           f=first_name_entry,
                           l=last_name_entry,
                           e=email_entry,
                           p=password_entry: self.on_signup_button_click(
                s, f, l, e, p
            )
        )
        signup_button.grid(row=4, column=0, columnspan=2, pady=10)

    def authenticate_user(self, email, password):
        login_url = f'{self.api_base_uri}/login/'
        data = {
            "email": email,
            "password": password,
        }

        try:
            response = requests.post(login_url, json=data)
            response.raise_for_status()
            access_token = response.json()['access_token']
            setattr(self, 'authorization', f'Bearer {access_token}')
            print("Login successful:", access_token)
            return access_token
        except requests.exceptions.RequestException as ex:
            print("Login failed:", ex)
            return None

    def on_login_btn_click(self, email_entry, password_entry, login_frame):
        email = email_entry.get()
        password = password_entry.get()

        if self.authenticate_user(email, password):
            # Close the login window
            self.root.focus_set()
            self.root.grab_set()
            self.root.grab_release()
            login_frame.destroy()
        else:
            error_label = tkinter.Label(
                login_frame,
                text="Invalid username or password",
                bg='white',
                fg='red'
            )
            error_label.grid(row=3, column=0, columnspan=2, pady=10)

    def create_login_page(self):
        login_frame = tkinter.Frame(
            self.root,
            width=300,
            height=200,
            bg="white",
            highlightbackground="black",
            highlightthickness=2
        )
        login_frame.place(x=250, y=200)

        email_label = tkinter.Label(
            login_frame,
            text="Email :",
            bg='white'
        )
        email_label.grid(row=0, column=0, padx=10, pady=10)
        email_entry = tkinter.Entry(
            login_frame,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1
        )
        email_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label = tkinter.Label(
            login_frame,
            text="Password:",
            bg='white'
        )
        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry = tkinter.Entry(
            login_frame,
            bg="white",
            highlightbackground="black",
            highlightthickness=1,
            borderwidth=1,
            show="*"
        )
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        login_button = tkinter.Button(
            login_frame,
            text="Login",
            command=lambda e=email_entry,
                           p=password_entry: self.on_login_btn_click(
                e,
                p,
                login_frame
            )
        )
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        signup_button = tkinter.Button(
            login_frame,
            text="Signup",
            command=self.create_signup_page
        )
        signup_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.root.wait_window(login_frame)

    def exe_func(self):
        login_page = self.create_login_page()

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
        text_label = tkinter.Label(
            self.root,
            text="Refresh in every",
            bg='white'
        )
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
            command=lambda link=link_input,
                           interval_period=interval_period: self.on_start_button_click(
                link, interval_period)
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
        rss_feed_text = tkinter.Label(self.root, text="Rss Feed List",
                                      bg='white', font=fontObj)
        rss_feed_text.place(x=20, y=160)
        self.root.mainloop()
