from googleapiclient.discovery import build
from google.oauth2 import service_account
from podio_api import PodioAPI
from datetime import datetime
import json

# Google API Credentials
SERVICE_ACCOUNT_FILE = "google.json"
SCOPES = ["https://www.googleapis.com/auth/admin.directory.group"]

# Initialize Google Admin SDK
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("admin", "directory_v1", credentials=creds)


def check_group_exists(email):
    try:
        group = service.groups().get(groupKey=email).execute()
        return group is not None
    except Exception as e:
        return False


# Function to check if an email is already a member of a group
def is_member_already(group_key, member_email):
    try:
        members = (
            service.members().list(groupKey=group_key).execute().get("members", [])
        )
        return any(member["email"] == member_email for member in members)
    except Exception as e:
        return False


# Function to create a Google Group (mailing list)
def create_google_group(email, name, description):
    group = {"email": email, "name": name, "description": description}
    return service.groups().insert(body=group).execute()


# Function to add a member to a Google Group
def add_member_to_group(group_key, member_email):
    if is_member_already(group_key, member_email):
        print(f"Member {member_email} is already a member of {group_key}.")
        return
    member = {"email": member_email, "role": "MEMBER"}
    service.members().insert(groupKey=group_key, body=member).execute()


def get_private_email(member):
    for field in member.get("fields", []):
        if field.get("label") == "Private Email Adresse":
            email_values = field.get("values", [])
            if email_values:
                return email_values[0].get("value")
    return None


def calculate_owed_amount(member, rate_per_six_months=25):
    for field in member.get("fields", []):
        if field.get("external_id") == "mitglied-beitrag-gezahlt-bis":
            paid_until_values = field.get("values", [])
            if paid_until_values:
                paid_until_str = paid_until_values[0].get("start_date")
                if paid_until_str:
                    paid_until_date = datetime.strptime(paid_until_str, "%Y-%m-%d")
                    current_date = datetime.now()
                    if current_date > paid_until_date:
                        days_owed = (current_date - paid_until_date).days
                        # 6 months = 182.5 days on average
                        months_owed = days_owed / 182.5
                        return round(months_owed * rate_per_six_months, 2)
    return 0


# Connect to Podio and fetch members
podio = PodioAPI("podio.json")
active_members = podio.get_all_members()

# Create a new Google Group
group_email = "spaceteam-members@spaceteam.at"
group_name = "Space Team Members"
group_description = "Mailing list for active Space Team members"
if not check_group_exists(group_email):
    group = create_google_group(group_email, group_name, group_description)

print("Count of emails which are going to be added: ", len(active_members))

# Add active members to the Google Group
for member in active_members:
    private_email = get_private_email(member)
    amount = calculate_owed_amount(member)
    if amount >= 50:
        continue
    print(private_email, ",", amount)
    add_member_to_group(group_email, private_email)

print("Mailing list created and members added.")
