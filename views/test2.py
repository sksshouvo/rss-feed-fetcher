import tkinter as tk

def on_select(event):
    selected_item = listbox.get(listbox.curselection())
    print(f"Selected item: {selected_item}")

# Create the main window
window = tk.Tk()
window.title("Listbox Example")

# Create a Listbox
listbox = tk.Listbox(window, selectmode=tk.SINGLE)
listbox.pack(pady=10)

# Add items to the Listbox
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
for item in items:
    listbox.insert(tk.END, item)

# Bind the selection event to a function
listbox.bind("<<ListboxSelect>>", on_select)

# Run the Tkinter event loop
window.mainloop()