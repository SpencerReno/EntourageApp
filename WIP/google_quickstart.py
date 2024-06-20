import os.path
from datetime import datetime
import pandas as pd 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
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
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    folder_id='15-aqS6s0fyTxCI8qva9Y0p4oXeeaIeFe'
    service = build("drive", "v3", credentials=creds)

    # first call for recent year folder 
    results = (
        service.files().list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)").execute() )
    items = results.get("files", [])

    if not items:
      return 'No Files found'


  #gets most recent Year folder
    recent_year_folder_id = str(items[0]['id'])
    service = build("drive", "v3", credentials=creds)
    results = (
        service.files()
      
        .list(supportsAllDrives=True, includeItemsFromAllDrives=True, q=f"parents in '{recent_year_folder_id}' and trashed = false", fields = "nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    most_recent_file = items[0]['name']
    most_recent_file=most_recent_file.split('.')[0]
    datetime_object = datetime.strptime(most_recent_file,'%m/%d/%y')
    start, end = datetime_object, datetime.now()
    missing_dates = [str(d).split(' ')[0] for d in pd.date_range(start, end) if d.weekday() == 2]
    print(missing_dates[1:])



  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()