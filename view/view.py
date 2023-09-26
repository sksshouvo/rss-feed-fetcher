# main.py
from dotenv import load_dotenv
from tkinter import *
# Load environment variables from .env file
load_dotenv()
# Now you can access environment variables using the os module
import os

class view:
    def __init__(self):
       self.faviconPath = './assets/images/favicon.png'
       self.appName     = os.getenv("APP_NAME")

    def exeFunc(self):
        root = Tk()
        img  = PhotoImage(file=self.faviconPath)
        root.iconphoto(False, img)
        root.title(self.appName)
        root.geometry("800x600")
        #Create a LabelFrame
        frame = Frame(root, width= 775, height= 200, bg= "white", highlightbackground="black", highlightthickness=2, borderwidth=2)
        #Configure the Frame
        frame.place(x=10, y=20)
        root.resizable(0,0)
        # Code to add widgets will go here...
        root.mainloop()
