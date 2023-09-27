# main.py
from dotenv import load_dotenv
from tkinter import *
from classes.validation import validation
from tkinter import messagebox
# Load environment variables from .env file
load_dotenv()
# Now you can access environment variables using the os module
import os

class view:
    def __init__(self):
       self.faviconPath = './assets/images/favicon.png'
       self.appName     = os.getenv("APP_NAME")

    def on_validate_input(self, P):
        # This function is called when the Entry widget is modified
        # Check if the input is a valid number with a maximum length of 2
        return P.isdigit() and len(P) <= 2
    
    def start_action(self, linkInput):
            entryText = linkInput.get()
            try:
                # Attempt to validate the entry
                validation.validate_entry(entryText)
            except ValueError as e:
                # Display an error message when validation fails
                messagebox.showerror("Error", str(e))
            pass

        
    def exeFunc(self):
        root = Tk()
        img  = PhotoImage(file=self.faviconPath)
        root.iconphoto(False, img)
        root.title(self.appName)
        root.geometry("800x600")
        #Create a LabelFrame
        frame = Frame(root, width=775, height=100, bg= "white", highlightbackground="black", highlightthickness=2, borderwidth=2)
        #Configure the Frame
        frame.place(x=10, y=20)
        # link entry field
        linkInput = Entry(root, bg= "white", highlightbackground="black", highlightthickness=1, borderwidth=1)
        linkInput.insert(0, "  Paste Your Rss Feed Link Here...")
        linkInput.place(x=20, y=40, width=750, height=30)
        root.resizable(0,0)
        #text field
        textLabel = Label(root, text = "Refresh in every", bg='white')
        textLabel.place(x=20, y=80)
        #interval count field
        intervelCountInput = Entry(root, bg= "white", highlightbackground="black", highlightthickness=1, borderwidth=1)
        intervelCountInput.place(x=120, y=80, width=35)
        validate_input = root.register(self.on_validate_input)
        intervelCountInput.config(validate="key", validatecommand=(validate_input, "%P"))

        # Dropdown menu options
        options = [
            "MIN",
            "HOUR",
            "DAYS",
            "MONTH"
        ]
        
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set("MIN")
        
        # Create Dropdown menu
        interval = OptionMenu( root , clicked , *options )
        interval.place(x=160, y=75)
        #start button
        startButton = Button(root, text ="Start", command=lambda entry=linkInput: self.start_action(entry))
        startButton.place(x=625, y=75, width=70, height=30)
        #start button
        stopButton = Button(root, text ="Stop")
        stopButton.place(x=700, y=75, width=70, height=30)
        # Code to add widgets will go here...
        root.mainloop()
