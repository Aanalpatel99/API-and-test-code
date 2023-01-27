# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2023-Jan-11 11:14:18
@author: Aanal Patel

:to keep the logs of the robot

NOTE: with this file, robot also need one .picke file inorder not have to authurize the api everytime.
    it will be generated firsttime code will run. 

"""

import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from glob import glob


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None

    pickle_file = pickle_file = 'token_' + API_SERVICE_NAME + '_' + API_VERSION + '.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

Client_Serect_File = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service_test = Create_Service(Client_Serect_File, API_NAME, API_VERSION, SCOPES)

file_name_csv = 'OrderServeDataFile.csv' 
mime_type_csv = 'text/csv' 
folder_ID = '1m2MDmK4n81rSsqnpFWp3IOR2zzwSt1UE' # folder where the files required to upload

file_metadata = {
  'name': file_name_csv, 
  'mimeType': mime_type_csv, 
  'parents': [folder_ID]
}

query = "name='{}' and trashed=false and parents='{}'".format(file_name_csv, folder_ID)
results = service_test.files().list(q=query,fields="nextPageToken, files(id, name)").execute()
filesOnDrive = results.get("files", [])

media = MediaFileUpload('{}'.format(file_name_csv), mimetype=mime_type_csv)

if not filesOnDrive:
    response = service_test.files().create(supportsTeamDrives=True, body=file_metadata, media_body=media, fields='id').execute()
else:
    file_id = filesOnDrive[0].get('id')
    response_update =  service_test.files().update(fileId=file_id, media_body=media, supportsTeamDrives=True).execute()

file_name_csv = 'Robot_RunTime.csv' 

file_metadata = {
  'name': file_name_csv, 
  'mimeType': mime_type_csv, 
  'parents': [folder_ID]
}

query = "name='{}' and trashed=false and parents='{}'".format(file_name_csv, folder_ID)
results = service_test.files().list(q=query,fields="nextPageToken, files(id, name)").execute()
filesOnDrive = results.get("files", [])

media = MediaFileUpload('{}'.format(file_name_csv), mimetype=mime_type_csv)
    
if not filesOnDrive:
    response = service_test.files().create(supportsTeamDrives=True, body=file_metadata, media_body=media, fields='id').execute()

else:
    file_id = filesOnDrive[0].get('id')
    response_update =  service_test.files().update(fileId=file_id, media_body=media, supportsTeamDrives=True).execute()

"""
list_of_files_zip = glob("./log/*.zip")
full_path = ["{0}".format(x) for x in list_of_files_zip]

for fileToUpload in full_path:
    service_test = Create_Service(Client_Serect_File, API_NAME, API_VERSION, SCOPES)
    base_file_name = os.path.basename(fileToUpload)
    file_name = base_file_name 
    mime_type = 'application/zip' 

    file_metadata = {
      'name': base_file_name, 
      'mimeType': 'application/zip', 
      'parents': ["15qA4YAZPGFcxFVtLOjgm8LE0j0aC-hvY"]
    }

    file_name = file_metadata['name']
    query = "name='{}' and trashed=false and parents='15qA4YAZPGFcxFVtLOjgm8LE0j0aC-hvY'".format(file_name)
    results = service_test.files().list(q=query,fields="nextPageToken, files(id, name)").execute()
    filesOnDrive = results.get("files", [])

    if not filesOnDrive:
        media = MediaFileUpload('./log/{}'.format(file_name), mimetype=mime_type)
        response = service_test.files().create(supportsTeamDrives=True, body=file_metadata, media_body=media, fields='id').execute()
    else:
        file_id = filesOnDrive[0].get('id')
        media = MediaFileUpload('./log/{}'.format(file_name), mimetype=mime_type)
        response_update =  service_test.files().update(fileId=file_id, media_body=media, supportsTeamDrives=True).execute()
"""
