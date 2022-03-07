from podio_api import PodioAPI
from google_api import GoogleAPI
from misc import gen_random_password
from user import User
import json

def main():
    podio = PodioAPI()
    google = GoogleAPI()
    
    print("Fetching members from podio ...")
    new_members = podio.get_new_members()
    print("done.")

    print(json.dumps(new_members[0]["fields"][6]["values"][0]["value"]))

    exit()
    for member in new_members:
        given_name = member["fields"][1]["values"][0]["value"]
        surname = member["fields"][2]["values"][0]["value"]
        recovery_email = member["fields"][5]["values"][0]["value"]
        phonenumber = member["fields"][6]["values"][0]["value"]
        podio_id = member["item_id"]

        print("Generating unique-ish password ...")
        password = gen_random_password(16)
        print("done.")
        print("Updating to \"in arbeit\" on podio ...")
        print(podio.change_state_of_member(podio_id, 4))
        print("done.")
        #TODO replace special letters
        user = User(
            email=given_name.lower()+'.'+surname.lower()+'@spaceteam.at',
            recovery_email=recovery_email,
            given_name = given_name,
            family_name = surname,
            password=password,
            phonenumber=phonenumber,
        )
        print("Creating user ...")
        print(google.create_new_account(user))
        print("done.")
        print("Add account to team_alt group ...")
        print(google.add_account_to_group("spaceteam@spaceteam.at", user.email))
        print("done.")
        # userinfo = {'primaryEmail': given_name.lower()+'.'+surname.lower()+'@spaceteam.at',
        #             'name': {'givenName': given_name, 'familyName': surname},
        #             'password': password, 
        #  'changePasswordAtNextLogin': True,
        # 'recoveryEmail': recovery_email,
        #'recoveryPhone': recovery_phone_number}
        print(userinfo)

if __name__ == "__main__":
    main()