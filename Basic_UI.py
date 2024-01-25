import tkinter as tk
import textwrap
import google.generativeai as genai

def on_send_button_click(event=None):
    message = entry.get()
    if message:
        # Insert the message at the end of the listbox
        messages_listbox.insert(tk.END, f"You: {message}")
        # Clear the entry widget after sending
        entry.delete(0, 'end')
        
        # Generate response using Generative AI
        response = model.generate_content(message)
        formatted_response = to_markdown(response.text)
        messages_listbox.insert(tk.END, formatted_response)

def to_markdown(text):
    # Format text as markdown
    formatted_text = text.replace('•', '  *')
    return textwrap.indent(formatted_text, 'Sahayak: ')

# Create the main window
window = tk.Tk()
window.title("Dharshak AI")

# Create and place the listbox widget
messages_listbox = tk.Listbox(window, width=40, height=10)
messages_listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

# Create and place the entry widget with a fixed width of 50
entry = tk.Entry(window, width=50)
entry.pack(padx=10, pady=10, side=tk.LEFT)  # Set side=tk.LEFT

# Create and place the "Send" button with a larger width and height
send_button = tk.Button(window, text="Send", command=on_send_button_click, width=10, height=2)
send_button.pack(pady=10, side=tk.LEFT)  # Set side=tk.LEFT

# Bind the <Return> key to the on_send_button_click function
entry.bind("<Return>", on_send_button_click)

# Allow the window to be resizable in both directions
window.resizable(True, True)

# Initialize Google Generative AI model
genai.configure(api_key='AIzaSyCMRX-gx13aEdKP4ko_dP5gppwHUFu-7Ec')
model = genai.GenerativeModel('gemini-pro')

# Start the main event loop
window.mainloop()
