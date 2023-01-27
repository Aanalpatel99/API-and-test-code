
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pickle import load, dump
from os.path import exists
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from glob import glob
from socket import gethostname
robot_name = gethostname()

def create_gmail_service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None

    pickle_file = pickle_file = 'token_' + API_SERVICE_NAME + '_' + API_VERSION + '.pickle'

    if exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

# Example usage
Client_Serect_File = 'client_secret_gmail.json'

API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

service_test = create_gmail_service(Client_Serect_File, API_NAME, API_VERSION, SCOPES)

def send_email(service, to, subject, body):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    message.attach(MIMEText(body))
    create_message = {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(F'sent message to {to} Message Id: {send_message["id"]}')

subject = 'Noreply: REBOOT ALERT'
msg = 'This email is system generated to notify developer that, the reboot has been performed by the user of the robot ' + robot_name 
send_email(service_test,'aanal.patel@petpooja.com',subject,msg)


