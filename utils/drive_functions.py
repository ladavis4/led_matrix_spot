from __future__ import print_function

import io
import os

from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def download_files(folder_id, local_folder_path, debug=False):
    """Downloads files from a specified directory. Requires a download_credentials.json file
    Args:
        folder_id: ID of the folder to download
        local_folder_path: path of the local folder to put the files
        debug: Enables print statements
    """
    creds = None
    if os.path.exists('credentials/download_token.json'):
        creds = Credentials.from_authorized_user_file('credentials/download_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/download_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials/download_token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Get info of all files in folder
        service = build('drive', 'v3', credentials=creds)
        query = f"parents ='{folder_id}'"
        response = service.files().list(q=query).execute()
        drive_files = response.get('files')
        drive_file_names = []

        for file in drive_files:
            drive_file_names.append(file['name'])

        # remove local files that are no longer in google drive folder
        local_files_to_delete = list(set(os.listdir(local_folder_path)) - set(drive_file_names))
        for local_file in local_files_to_delete:
            os.remove(os.path.join(local_folder_path, local_file))
            if debug:
                print(f"Removed {local_file}")
            
        for file in drive_files:
            local_file_path = os.path.join(local_folder_path, file['name'])
            # Check if file exists already
            if not os.path.exists(local_file_path):
                request = service.files().get_media(fileId=file['id'])
                file_io = io.BytesIO()
                downloader = MediaIoBaseDownload(file_io, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()

                with open(local_file_path, "wb") as f:
                    f.write(file_io.getbuffer())
                    
                if debug:
                    print(f"Downloaded {file['name']}")
            else:
                if debug:
                    print(f'File {file["name"]} already exists')

    except HttpError as error:
        print(F'An error occurred: {error}')


if __name__ == '__main__':
    download_files(folder_id='1PRMe_4aRs3K1INoxURx7EUKPkkU0C6Mq', 
                   local_folder_path=os.path.join(os.getcwd(), "images"), debug=True)
