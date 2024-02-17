from tkinter import messagebox
import re
import ttkbootstrap as ttk
import tkinter as tk
from abc import ABC
from config.settings import AUTH_PASSWORD_VALIDATORS


class Authentication(ABC):

    def on_entry_focus_in(self, event):
        # if event.widget.get() == self.email_placeholder or event.widget.get() == self.password_placeholder:
        event.widget.delete(0, tk.END)
        if event.widget == self.password_entry or (
                        hasattr(self, 'confirm_password_entry') and
                        event.widget == self.confirm_password_entry
        ):
            event.widget.config(show='*')

    def on_entry_focus_out(self, event):
        if not event.widget.get():
            if hasattr(self, 'email_entry') and event.widget == self.email_entry:
                event.widget.insert(0, self.email_placeholder)
            elif hasattr(self, 'password_entry') and event.widget == self.password_entry:
                event.widget.config(show='')
                event.widget.insert(0, self.password_placeholder)
            elif hasattr(self, 'name_entry') and event.widget == self.name_entry:
                event.widget.config(show='')
                event.widget.insert(0, self.name_placeholder)
            elif hasattr(self, 'confirm_password_entry') and event.widget == \
                    self.confirm_password_entry:
                event.widget.config(show='')
                event.widget.insert(0, self.confirm_password_placeholder)

    def make_input_entry(self, name, placeholder='', *args, **kwargs):
        # self.email_placeholder = placeholder
        plcaholder_attr = f'{name.replace(" ", "_")}_placeholder'
        input_entry_attr = f'{name}_entry'

        setattr(self, plcaholder_attr, placeholder)
        # self.email_entry = ttk.Entry(self.frame, width=45)
        setattr(self, input_entry_attr, ttk.Entry(self.frame, width=45))
        field = getattr(self, input_entry_attr)

        field.insert(0, getattr(self, plcaholder_attr))
        # self.email_entry.insert(0, self.email_placeholder)
        field.bind("<FocusIn>", self.on_entry_focus_in)
        # self.email_entry.bind("<FocusIn>", self.on_entry_focus_in)
        field.bind("<FocusOut>", self.on_entry_focus_out)
        # self.email_entry.bind("<FocusOut>", self.on_entry_focus_out)
        field.pack(pady=(0, 10))
        # self.email_entry.pack(pady=(0, 10))

class LoginView(Authentication):
    def __init__(self, master=None):
        if not master:
            master = ttk.Window(themename='litera')
        self.master = master
        self.initialize_login_view()

    def initialize_login_view(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title('Login - Rss Feed Fetcher')

        self.feed_fetcher_label = ttk.Label(
            self.master,
            text='Rss Feed Fetcher',
            font=('Arial', 18),
            anchor='center'
        )
        self.feed_fetcher_label.pack(pady=(10, 0))

        self.outer_frame = ttk.Frame(
            self.master,
            borderwidth=2,
            relief='groove'
        )
        self.outer_frame.pack(padx=20, pady=10)

        self.frame = ttk.Frame(self.outer_frame)
        self.frame.pack(padx=20, pady=20)

        self.title = ttk.Label(
            self.frame,
            text='Login',
            font=('Arial', 12, 'bold')
        )
        self.title.pack(pady=(0, 20))

        self.make_input_entry("email", "Email")
        self.make_input_entry("password", "Password")

        self.login_button = ttk.Button(
            self.frame,
            text='Login',
            bootstyle='success',
            command=self.login,
            width=16
        )
        self.login_button.pack(pady=(0, 10))

        self.forgot_password_label = ttk.Label(
            self.frame,
            text='Forgot Password ?',
            foreground='blue',  # Set the text color
            cursor='hand2',  # Set the cursor to a pointing hand
        )
        self.forgot_password_label.pack(pady=(0, 10))

        self.separator = ttk.Label(self.master, text='Or')
        self.separator.pack(pady=(0, 10))

        self.register_button = ttk.Button(
            self.master,
            text='Register',
            bootstyle='primary',
            command=self.switch_to_register,
            width=16
        )
        self.register_button.pack(pady=(10, 20))

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validation
        if not self.validate_email(email):
            messagebox.showerror('Invalid Email',
                                 'Please enter a valid email address.')
            return
        if not self.validate_password(password):
            messagebox.showerror('Invalid Password',
                                 'Password cannot be empty.')
            return

        #ToDo : Actual Login Logic and API call goes here

        messagebox.showinfo(
            'Login Attempt',
            f'Email: {email}Password: {password}'
        )

    def validate_email(self, email):
        if email and re.match(r'^\S+@\S+\.\S+$', email):
            return True
        return False

    def validate_password(self, password):
        return bool(password)

    def switch_to_register(self):
        self.registration_view = RegistrationView(self.master)


class RegistrationView(Authentication):
    def __init__(self, master):
        self.master = master
        self.initialize_registration_view()

    def initialize_registration_view(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title('Login - Rss Feed Fetcher')

        self.feed_fetcher_label = ttk.Label(
            self.master,
            text='Rss Feed Fetcher',
            font=('Arial', 18),
            anchor='center'
        )
        self.feed_fetcher_label.pack(pady=(10, 0))

        self.outer_frame = ttk.Frame(
            self.master,
            borderwidth=2,
            relief='groove'
        )
        self.outer_frame.pack(padx=20, pady=10)

        self.frame = ttk.Frame(self.outer_frame)
        self.frame.pack(padx=20, pady=20)

        self.title = ttk.Label(
            self.frame,
            text='Register',
            font=('Arial', 12, 'bold')
        )
        self.title.pack(pady=(0, 20))

        self.make_input_entry("name", "Name")
        self.make_input_entry("email", "Email")
        self.make_input_entry("password", "Password")
        self.make_input_entry("confirm_password", "Confirm_password")

        self.register_button = ttk.Button(
            self.frame,
            text='Register',
            bootstyle='primary',
            command=self.register,
            width=16
        )
        self.register_button.pack(pady=(0, 10))

        self.separator = ttk.Label(self.master, text='Or')
        self.separator.pack(pady=(0, 10))

        self.login_button = ttk.Button(
            self.master,
            text='Login',
            bootstyle='success',
            command=self.switch_to_login,
            width=16
        )
        self.login_button.pack(pady=(5, 20))

    def validate_name(self, name):
        if not name or name.isdigit() or not name.isalpha():
            return False
        return True

    def validate_email(self, email):
        if email and re.match(r'^\S+@\S+\.\S+$', email):
            return True
        return False

    def validate_password(self, password):
        if (
                len(password) >= 8 and
                re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[\W_]', password)
        ):
            return True
        return False

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validation
        if not self.validate_name(name):
            messagebox.showerror(
                'Invalid Name',
                'Name cannot be empty, a number, and must be a valid string.'
            )
            return
        if not self.validate_email(email):
            messagebox.showerror(
                'Invalid Email',
                'Please enter a valid email address.'
            )
            return
        if not self.validate_password(password):
            for validator in AUTH_PASSWORD_VALIDATORS:
                validator = validator()
                result = validator.validate(password, messagebox)
                if not result:
                    break

            # messagebox.showerror(
            #     'Invalid Password',
            #     'Password must be at least 8 characters long, '
            #     'contain a capital and a lower case letter, a symbol, '
            #     'and a number.'
            # )
            return
        if password != confirm_password:
            messagebox.showerror(
                'Password Mismatch',
                'Confirm Password does not match with Password.'
            )
            return

        # ToDo :  Actual Register Logic and API calls goes here

        messagebox.showinfo(
            'Register Attempt',
            'Registration logic goes here.'
        )

    def switch_to_login(self):
        self.login_view = LoginView(self.master)


if __name__ == "__main__":
    root = ttk.Window(themename='litera')
    login_view = LoginView(root)
    root.mainloop()
