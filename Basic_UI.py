import tkinter as tk

def on_send_button_click(event=None):
    message = entry.get()
    if message:
        # Insert the message at the end of the listbox
        messages_listbox.insert(tk.END, f"You: {message}")
        # Clear the entry widget after sending
        entry.delete(0, 'end')

# Create the main window
window = tk.Tk()
window.title("Chat UI")

# Create and place the listbox widget
messages_listbox = tk.Listbox(window, width=40, height=10)
messages_listbox.pack(padx=30, pady=30, expand=True, fill=tk.BOTH)

# Create and place the entry widget with a fixed width of 50
entry = tk.Entry(window, width=100)
entry.pack(padx=30, pady=10, side=tk.LEFT)  # Set side=tk.LEFT

# Create and place the "Send" button with a larger width and height
send_button = tk.Button(window, text="Send", command=on_send_button_click, width=10, height=3)
send_button.pack(padx=30, pady=10, side=tk.LEFT)  # Set side=tk.LEFT

# Bind the <Return> key to the on_send_button_click function
entry.bind("<Return>", on_send_button_click)

# Allow the window to be resizable in both directions
window.resizable(True, True)

# Start the main event loop
window.mainloop()
