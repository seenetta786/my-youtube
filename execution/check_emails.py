
import argparse
import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def check_emails(sender):
  """Checks for unread emails from a specific sender.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    
    # search for unread emails from the sender
    query = f"is:unread from:{sender}"
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if "messages" in result:
      messages.extend(result["messages"])
    
    for message in messages:
      msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
      payload = msg['payload']
      parts = payload.get('parts')
      
      data = ""
      if parts:
          for part in parts:
              if part['mimeType'] == 'text/plain':
                  data = part['body']['data']
                  break
      else:
          data = payload['body']['data']

      if data:
        # data is base64 encoded
        text = base64.urlsafe_b64decode(data).decode('utf-8')
        print(text)

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for new emails.")
    parser.add_argument("sender", help="The sender's email address to check for.")
    
    args = parser.parse_args()
    
    check_emails(args.sender)
