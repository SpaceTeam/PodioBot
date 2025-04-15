from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from user import User


SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group.member",
]


class GoogleAPI:
    def __init__(self, config_name: str) -> None:
        creds = None
        if os.path.exists(config_name):
            creds = Credentials.from_service_account_file(config_name, scopes=SCOPES)

        self.service = build("admin", "directory_v1", credentials=creds)

    def create_new_account(self, user: User) -> str:
        info = {
            "primaryEmail": user.email,
            "name": {
                "givenName": user.given_name,
                "familyName": user.family_name,
            },
            "password": user.password,
            "changePasswordAtNextLogin": True,
            "recoveryEmail": user.recovery_email,
        }
        
        try:
            # Try to create new account
            return self.service.users().insert(body=info).execute()
        except Exception as e:
            if "Entity already exists" in str(e):
                # Account exists, try to update it
                update_info = info.copy()
                del update_info['primaryEmail']  # Can't update primary email
                try:
                    return self.service.users().update(userKey=user.email, body=update_info).execute()
                except Exception as update_e:
                    raise update_e
            raise e

    def add_account_to_group(
        self, groupkey: str, email: str
    ) -> str:  # group key e.g email or id of group
        payload = {
            "email": email,
        }
        try:
            return self.service.members().insert(groupKey=groupkey, body=payload).execute()
        except Exception as e:
            if "Member already exists" in str(e):
                # Member is already in the group, this is fine
                return f"User {email} is already a member of {groupkey}"
            raise e
