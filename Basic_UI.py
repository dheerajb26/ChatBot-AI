import tkinter as tk
from tkinter import filedialog
import textwrap
import google.generativeai as genai
import fitz
from exchangelib import Credentials, Account, DELEGATE, Configuration

def extract_text_from_pdf_bytes(pdf_bytes):
    text = ""
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf_document:
            for page in pdf_document:
                text += page.get_text()
    except Exception as e:
        text = f"Error extracting text from PDF: {str(e)}"
    return text

def generate_summary(text):
    # Generate summary using Generative AI
    response = model.generate_content(text)
    formatted_response = to_markdown(response.text)
    return formatted_response

def fetch_and_generate_summaries(email, password):
    # Set up credentials and connect to Outlook account
    credentials = Credentials(email, password)

    # Specify the EWS endpoint manually (replace with the correct endpoint)
    ews_url = 'outlook.office365.com'

    # Create a configuration with the EWS url
    config = Configuration(server=ews_url, credentials=credentials)

    # Use the configuration when creating the Account
    account = Account(primary_smtp_address=email, config=config, autodiscover=False, access_type=DELEGATE)

    # Fetch all emails
    emails = list(account.inbox.all())

    # Generate and display summary for each email
    messages_text.config(state=tk.NORMAL)
    messages_text.delete(1.0, tk.END)  # Clear existing content

    for i, email in enumerate(emails, 1):
        messages_text.insert(tk.END, f"Email {i}:\n")
        messages_text.insert(tk.END, f"Subject: {email.subject}\n")
        messages_text.insert(tk.END, f"From: {email.sender.email_address}\n")
        messages_text.insert(tk.END, f"Received: {email.datetime_received}\n")

        if email.text_body:
            # If the email has text content, generate a summary
            summary = generate_summary(email.text_body)
            messages_text.insert(tk.END, f"Summary:\n{summary}\n")

        messages_text.insert(tk.END, "-" * 50 + "\n")

    messages_text.config(state=tk.DISABLED)

def on_email_entry_click(event):
    if entry_email.get() == "Enter your email":
        entry_email.delete(0, tk.END)
        entry_email.config(fg='black')  # Change text color to black

def on_password_entry_click(event):
    if entry_password.get() == "Enter your password":
        entry_password.delete(0, tk.END)
        entry_password.config(show='*')  # Show '*' for password characters
        entry_password.config(fg='black')  # Change text color to black

def to_markdown(text):
    formatted_text = text.replace('•', '  *')
    return textwrap.indent(formatted_text, 'Sahayak: ')

def on_fetch_and_summarize_button_click():
    email = entry_email.get()
    password = entry_password.get()
    fetch_and_generate_summaries(email, password)

window = tk.Tk()
window.title("Dharshak AI")

messages_text = tk.Text(window, width=80, height=20, wrap=tk.WORD, state=tk.DISABLED)
yscroll = tk.Scrollbar(window, orient=tk.VERTICAL, command=messages_text.yview)
messages_text.config(yscrollcommand=yscroll.set)
messages_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
yscroll.pack(side=tk.RIGHT, fill=tk.Y)

# Entry field for email with placeholder text
entry_email = tk.Entry(window, width=30, fg='grey')
entry_email.insert(0, "Enter your email")
entry_email.bind("<FocusIn>", on_email_entry_click)
entry_email.pack(padx=10, pady=5, side=tk.LEFT)

# Entry field for password with placeholder text
entry_password = tk.Entry(window, width=30, show='', fg='grey')
entry_password.insert(0, "Enter your password")
entry_password.bind("<FocusIn>", on_password_entry_click)
entry_password.pack(padx=10, pady=5, side=tk.LEFT)

fetch_and_summarize_button = tk.Button(window, text="Fetch and Summarize", command=on_fetch_and_summarize_button_click, width=20, height=2)
fetch_and_summarize_button.pack(pady=10, side=tk.LEFT)

window.resizable(True, True)

# Set up Generative AI model
genai.configure(api_key='AIzaSyCMRX-gx13aEdKP4ko_dP5gppwHUFu-7Ec')
model = genai.GenerativeModel('gemini-pro')

window.mainloop()
