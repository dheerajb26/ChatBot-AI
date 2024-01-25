import tkinter as tk
import openai  # You need to install the 'openai' library (pip install openai)

# Set your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'

def get_chatbot_response(message):
    # Make a request to the OpenAI API for a chat-based response
    response = openai.Completion.create(
        engine="text-davinci-002",  # You may use a different engine if needed
        prompt=message,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def on_send_button_click(event=None):
    user_message = entry.get()
    if user_message:
        # Display the user's message in the listbox
        messages_listbox.insert(tk.END, f"You: {user_message}")

        # Get the chatbot's response
        bot_response = get_chatbot_response(user_message)

        # Display the chatbot's response in the listbox
        messages_listbox.insert(tk.END, f"Chatbot: {bot_response}")

        # Clear the entry widget after sending
        entry.delete(0, 'end')

# Create the main window
window = tk.Tk()
window.title("Chat UI")

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

# Start the main event loop
window.mainloop()
