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

def on_upload_button_click():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Process the uploaded file (you can add your logic here)
        messages_listbox.insert(tk.END, f"You uploaded: {file_path}")

def on_link_button_click():
    link = link_entry.get()
    if link:
        # Insert the link at the end of the listbox
        messages_listbox.insert(tk.END, f"You sent a link: {link}")

        # Generate response using Generative AI
        response = model.generate_content(link)
        formatted_response = to_markdown(response.text)
        messages_listbox.insert(tk.END, formatted_response)

        # Clear the entry widgets after sending
        entry.delete(0, 'end')
        link_entry.delete(0, 'end')

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

# Create and place the entry widget for regular messages
entry = tk.Entry(window, width=50)
entry.pack(padx=10, pady=10, side=tk.LEFT)

# Create and place the "Send" button for regular messages
send_button = tk.Button(window, text="Send", command=on_send_button_click, width=10, height=2)
send_button.pack(pady=10, side=tk.LEFT)

# Create and place the entry widget for links
link_entry = tk.Entry(window, width=50)
link_entry.pack(padx=10, pady=10, side=tk.LEFT)

# Create and place the "Send" button for links
link_button = tk.Button(window, text="Send Link", command=on_link_button_click, width=10, height=2)
link_button.pack(pady=10, side=tk.LEFT)

# Create and place the "Upload" button
upload_button = tk.Button(window, text="Upload", command=on_upload_button_click, width=10, height=2)
upload_button.pack(pady=10, side=tk.LEFT)

# Bind the <Return> key to the on_send_button_click function
entry.bind("<Return>", on_send_button_click)

# Allow the window to be resizable in both directions
window.resizable(True, True)

# Initialize Google Generative AI model
genai.configure(api_key='AIzaSyCMRX-gx13aEdKP4ko_dP5gppwHUFu-7Ec')
model = genai.GenerativeModel('gemini-pro')

# Start the main event loop
window.mainloop()
