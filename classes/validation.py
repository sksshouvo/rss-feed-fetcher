import tkinter as tk
from tkinter import messagebox

class validation:
   def validate_entry(entry_text):
        if not entry_text.strip():  # Check if the Entry is empty or contains only whitespace
            messagebox.showwarning("Warning", "Entry field cannot be empty.")
            return False
        return True
    