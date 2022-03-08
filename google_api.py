from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from user import User


SCOPES = ['https://www.googleapis.com/auth/admin.directory.user','https://www.googleapis.com/auth/admin.directory.group.member']


class GoogleAPI:
    def __init__(self, config_name: str) -> None:
        creds = None
        if os.path.exists(config_name):
            creds = Credentials.from_service_account_file(
                config_name, scopes=SCOPES)

        self.service = build('admin', 'directory_v1', credentials=creds)

    def create_new_account(self, user: User) -> str:
        info = {
            'primaryEmail': user.email,
            'name': {
                'givenName': user.given_name, 'familyName': user.family_name,
            },
            'password': user.password,
            'changePasswordAtNextLogin': True,
            'recoveryEmail': user.recovery_email,
            }
        return self.service.users().insert(body=info).execute()

    def add_account_to_group(self, groupkey: str, email: str) -> str: #group key e.g email or id of group
        payload = {
            'email' : email,
        }
        return self.service.members().insert(groupKey=groupkey, body=payload).execute()

    # results = service.users().list(domain="spaceteam.at", maxResults=10,
    #                                orderBy='email').execute()
    # users = results.get('users', [])

    # if not users:
    #     print('No users in the domain.')
    # else:
    #     print('Users:')
    #     for user in users:
    #         print(u'{0} ({1})'.format(user['primaryEmail'],
    #                                   user['name']['fullName']))

    # userinfo = {'primaryEmail': 'test10302@spaceteam.at',
    #             'name': {'givenName': 'Jane', 'familyName': 'Smith'},
    #             'password': '34gjklre304iojlo24j2kl3kdlj', }
