from tkinter import messagebox


class Validation:

    @staticmethod
    def validate_entry(entry_text):
        if not entry_text.strip():
            messagebox.showwarning("Warning", "Entry field cannot be empty.")
            return False
        return True
