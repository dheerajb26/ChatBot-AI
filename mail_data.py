from exchangelib import Credentials, Account, DELEGATE, Configuration

def sync_outlook_emails(username, password):
    # Replace these with your Outlook email address and password
    email = username
    password = password

    # Set up credentials and connect to Outlook account
    credentials = Credentials(email, password)

    # Specify the EWS endpoint manually (replace with the correct endpoint)
    ews_url = 'outlook.office365.com'

    # Create a configuration with the EWS url
    config = Configuration(server=ews_url, credentials=credentials)

    # Use the configuration when creating the Account
    account = Account(primary_smtp_address=email, config=config, autodiscover=False, access_type=DELEGATE)

    # Store emails in a dictionary with message ID as the key
    emails = {item.message_id: item for item in account.inbox.filter(is_read=False).order_by('-datetime_received')[:5]}

    # Print the entire dictionary
    for message_id, item in emails.items():
        print(f"Message ID: {message_id}, Subject: {item.subject}, From: {item.sender}, Received: {item.datetime_received}")
        print(f"Content: {item.text_body}")
        print("-----")

if __name__ == "__main__":
    # Replace 'your_email' and 'your_password' with your Outlook email address and password
    sync_outlook_emails('dheerajbalabadra26@outlook.com', '8143712410d')
