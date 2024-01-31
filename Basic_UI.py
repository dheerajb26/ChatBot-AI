import tkinter as tk
from tkinter import filedialog
import textwrap
import google.generativeai as genai
import fitz  # PyMuPDF for PDF text extraction
import re
import requests
import msal

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            num_pages = pdf_document.page_count
            for page_num in range(num_pages):
                page = pdf_document[page_num]
                text += page.get_text()
    except Exception as e:
        text = f"Error extracting text from PDF: {str(e)}"
    return text

def fetch_onedrive_file(client_id, tenant_id, client_secret, file_id):
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )

    # Get an access token
    token_response = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
    access_token = token_response['access_token']

    # Construct the API endpoint for file content
    endpoint = f'https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content'

    try:
        response = requests.get(endpoint, headers={'Authorization': 'Bearer ' + access_token})
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching file from OneDrive: {str(e)}"

def on_send_button_click(event=None):
    message = entry.get()
    if message:
        messages_text.config(state=tk.NORMAL)
        messages_text.insert(tk.END, f"You: {message}\n")
        messages_text.config(state=tk.DISABLED)
        entry.delete(0, 'end')

        response = model.generate_content(message)
        formatted_response = to_markdown(response.text)
        messages_text.config(state=tk.NORMAL)
        messages_text.insert(tk.END, formatted_response + '\n')
        messages_text.config(state=tk.DISABLED)

def on_upload_button_click():
    file_path = filedialog.askopenfilename()
    if file_path:
        messages_text.config(state=tk.NORMAL)
        messages_text.insert(tk.END, f"You uploaded: {file_path}\n")
        messages_text.config(state=tk.DISABLED)

        # Process the uploaded file and generate a summary
        if file_path.endswith(".pdf"):
            # If it's a PDF file, read the content using PyMuPDF
            pdf_text = extract_text_from_pdf(file_path)
        else:
            # For other file types, you may need to implement the appropriate logic
            pdf_text = "Unsupported file type. Unable to extract text."

        # Generate summary using Generative AI
        response = model.generate_content(pdf_text)
        formatted_response = to_markdown(response.text)
        messages_text.config(state=tk.NORMAL)
        messages_text.insert(tk.END, formatted_response + '\n')
        messages_text.config(state=tk.DISABLED)

def on_link_button_click():
    link = link_entry.get()
    if link:
        messages_text.config(state=tk.NORMAL)
        messages_text.insert(tk.END, f"You sent a link: {link}\n")
        messages_text.config(state=tk.DISABLED)

        # Check if it's a OneDrive link
        if "1drv.ms" in link:
            # Extract file ID from the OneDrive link
            match = re.search(r'(?<=\?id=)[\w-]+', link)
            if match:
                file_id = match.group(0)
            else:
                messages_text.insert(tk.END, "Error: Unable to extract file ID from OneDrive link\n")
                messages_text.config(state=tk.DISABLED)
                return

            # Fetch content from the OneDrive file
            document_content = fetch_onedrive_file(client_id, tenant_id, client_secret, file_id)

            if "Error fetching file from OneDrive" in document_content:
                messages_text.insert(tk.END, f"{document_content}\n")
                messages_text.config(state=tk.DISABLED)
                return

            # Generate summary using Generative AI
            try:
                response = model.generate_content(document_content)
                formatted_response = to_markdown(response.text)
                messages_text.config(state=tk.NORMAL)
                messages_text.insert(tk.END, formatted_response + '\n')
                messages_text.config(state=tk.DISABLED)
            except Exception as e:
                messages_text.insert(tk.END, f"Error generating content: {str(e)}\n")
                messages_text.config(state=tk.DISABLED)

            link_entry.delete(0, 'end')
        else:
            messages_text.insert(tk.END, "Error: Unsupported link format\n")
            messages_text.config(state=tk.DISABLED)
            return


def to_markdown(text):
    formatted_text = text.replace('•', '  *')
    return textwrap.indent(formatted_text, 'Sahayak: ')

window = tk.Tk()
window.title("Dharshak AI")

messages_text = tk.Text(window, width=40, height=10, wrap=tk.WORD, state=tk.DISABLED)
yscroll = tk.Scrollbar(window, orient=tk.VERTICAL, command=messages_text.yview)
messages_text.config(yscrollcommand=yscroll.set)
messages_text.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
yscroll.pack(side=tk.RIGHT, fill=tk.Y)

entry = tk.Entry(window, width=50)
entry.pack(padx=10, pady=10, side=tk.LEFT)

send_button = tk.Button(window, text="Send", command=on_send_button_click, width=10, height=2)
send_button.pack(pady=10, side=tk.LEFT)

link_entry = tk.Entry(window, width=50)
link_entry.pack(padx=10, pady=10, side=tk.LEFT)

link_button = tk.Button(window, text="Send Link", command=on_link_button_click, width=10, height=2)
link_button.pack(pady=10, side=tk.LEFT)

upload_button = tk.Button(window, text="Upload", command=on_upload_button_click, width=10, height=2)
upload_button.pack(pady=10, side=tk.LEFT)

entry.bind("<Return>", on_send_button_click)
window.resizable(True, True)

genai.configure(api_key='AIzaSyCMRX-gx13aEdKP4ko_dP5gppwHUFu-7Ec')
model = genai.GenerativeModel('gemini-pro')

window.mainloop()
