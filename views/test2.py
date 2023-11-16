import tkinter as tk
import sqlite3
import webbrowser
from tkinter import messagebox

class RssReaderApp:
    def __init__(self, master):
        self.master = master
        master.title("RSS Reader")

        # Connect to the SQLite database
        self.conn = sqlite3.connect('databases/rss_feed.db')  # Replace 'your_database.db' with your actual database name
        self.cursor = self.conn.cursor()

        # Fetch data from the 'new_rss_feeds' table
        self.cursor.execute('SELECT * FROM new_rss_feeds')
        self.data = self.cursor.fetchall()

        # Create a Listbox
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10)

        # Add items to the Listbox
        for item in self.data[:10]:  # Display only the first 10 rows
            self.listbox.insert(tk.END, item[1])  # Assuming 'title' is in the second column

        # Bind the selection event to a function
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)
            link = self.data[selected_index[0]][2]  # Assuming 'link' is in the third column
            confirmation = messagebox.askyesno("Confirmation", f"Do you want to open the link:\n{link}?")
            if confirmation:
                # Open the link in the default web browser
                webbrowser.open_new_tab(link)

    def __del__(self):
        # Close the database connection when the instance is deleted
        self.conn.close()

# Create the main window
root = tk.Tk()

# Create an instance of the RssReaderApp class
app = RssReaderApp(root)

# Run the Tkinter event loop
root.mainloop()
