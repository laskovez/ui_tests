import base64
import os
from datetime import datetime, timedelta
from time import sleep

import httplib2
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors, discovery  # needed for gmail service

from constants.common import Gmail
from utils.utils import set_filepath


class SendMail:
    SCOPES = ['https://mail.google.com/']
    client_secret_file = set_filepath('credentials.json', 'utils', 'gmail_api')

    def __init__(self):
        self.http = httplib2.Http()
        self.service = discovery.build('gmail', 'v1', credentials=self.get_credentials())
        self.credentials = self.get_credentials()
        self.last_read_message_id = None

    def get_credentials(self):
        credential_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(credential_path):
            credentials = Credentials.from_authorized_user_file(credential_path, self.SCOPES)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if os.path.exists(self.client_secret_file):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secret_file, self.SCOPES)
                    credentials = flow.run_local_server(port=0)
                else:
                    raise FileNotFoundError(
                        '\nNot found credentials.json file. '
                        '\nPlease, get auth credentials.json file at '
                        'https://developers.google.com/gmail/api/quickstart/python'
                        '\nand place it into scripts/gmail_api folder. All actions will be performed under your acc')
            # Save the credentials for the next run
            with open(credential_path, 'w') as token:
                token.write(credentials.to_json())

        return credentials

    @staticmethod
    def __decode_email_body(data: str, as_text=True):
        clean_one = data.replace('-', '+')  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace('_', '/')  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
        soup = BeautifulSoup(clean_two, 'html.parser')
        if as_text:
            soup = soup.text
        return soup

    def read_message(self, message_from=Gmail.EMAIL_FROM_FILTER, label_ids=None,
                     contains=None, exclude=None, include_spam_trash=True, after: int = None,
                     before: int = None):
        """after/before : takes timestamp value"""

        def construct_query():
            query = []
            if message_from:
                query.append(f'from:{message_from}')
            if exclude:
                query.append(f'-{exclude}')
            if contains:
                query.append(f'{contains}')
            if after:
                query.append(f'after:{after}')
            if before:
                query.append(f'before:{before}')
            r = ' '.join([str(i) for i in query])
            print(r)
            return r

        results = self.service.users().messages().list(
            userId='me',
            maxResults=1,
            labelIds=label_ids if label_ids else [],
            q=construct_query(),
            includeSpamTrash=include_spam_trash
        ).execute()
        try:
            # get the message id from the results object
            message_id = results['messages'][0]['id']
            self.last_read_message_id = message_id
            # use the message id to get the actual message, including any attachments
            message = self.service.users().messages().get(userId='me', id=message_id).execute()
            print('Message', str(message))
            print('Message snippet: %s' % message['snippet'])
            data = {'msg_id': message['id'], 'msg_snippet': message['snippet'], 'attachments': []}
            message_data = message['payload']['parts'][1]['body']['data']
            data['msg_body'] = self.__decode_email_body(message_data, as_text=False)

            return data

        except errors.HttpError:
            print('An error occurred')
        except KeyError as e:
            print(e)
            print('Email message not found...')

    def delete_message(self, message_id):
        try:
            self.service.users().messages().delete(userId='me', id=message_id).execute()
            print('Message with id: {} deleted successfully.'.format(message_id))
        except errors.HttpError as error:
            print('An error occurred: {}'.format(error))

    def wait_and_read_message(self, message_from=Gmail.EMAIL_FROM_FILTER, label_ids=None,
                              contains=None, exclude=None, include_spam_trash=True, delete_after_read=True,
                              after=None, before: int = None, await_time_seconds=Gmail.EMAIL_AWAIT_TIME_SECONDS):
        if after is None:
            after = datetime.timestamp(datetime.now().replace(microsecond=0))
        delay_seconds = 5
        while await_time_seconds:
            sleep(delay_seconds)
            time_after = datetime.timestamp(datetime.fromtimestamp(after) - timedelta(seconds=await_time_seconds))
            message = self.read_message(message_from=message_from, label_ids=label_ids, contains=contains,
                                        exclude=exclude, include_spam_trash=include_spam_trash, after=int(time_after),
                                        before=before)
            try:
                if not message:
                    await_time_seconds -= delay_seconds
                    continue
                return message
            finally:
                if delete_after_read and message:
                    self.delete_message(message_id=message['msg_id'])
        raise errors.InvalidNotificationError(
            f'Email message was not found in {Gmail.EMAIL_AWAIT_TIME_SECONDS} seconds;')
