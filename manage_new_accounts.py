from podio_api import PodioAPI
from google_api import GoogleAPI
from mail import MailSender
from misc import gen_random_password
from ascii import translate_to_ascii
from user import User

def manage_new_accounts():
    podio = PodioAPI('podio.json')
    google = GoogleAPI('google.json')
    mail_sender = MailSender('mail.json')
    
    print("Fetching members from podio ...")
    new_members = podio.get_new_members()
    print("done.")
    
    if len(new_members) == 0:
        print("No new members found.")
        exit()

    for member in new_members:
        given_name = podio.get_value_of_field_with_id(206982183,member)
        surname = podio.get_value_of_field_with_id(206982184,member)
        recovery_email = podio.get_value_of_field_with_id(206982186,member)
        podio_id = member["item_id"]
        
        print("Generating unique-ish password ...")
        password = gen_random_password(16)
        print("done.")
        print("Updating to \"in arbeit\" on podio ...")
        print(podio.change_state_of_member(podio_id, 4))
        print("done.")
        user = User(
            email=translate_to_ascii(given_name.lower()+'.'+surname.lower())+'@spaceteam.at',
            recovery_email=recovery_email,
            given_name = given_name,
            family_name = surname,
            password=password,
        )
        print("Creating user ...")
        print(google.create_new_account(user))
        print("done.")
        print("Updating email in podio ...")
        print(podio.update_st_email(podio_id,user))
        print("done.")
        print("Add account to spaceteam group ...")
        print(google.add_account_to_group("spaceteam@spaceteam.at", user.email))
        print("done.")
        print("Sending welcome mail ...")
        mail_sender.send_welcome_mail(user)
        print("done.")
        print("Updating begin of membership ...")
        print(podio.update_begin_of_membership(podio_id))
        print("done.")
        print("Updating to \"Neu\" on podio ...")
        print(podio.change_state_of_member(podio_id, 1))
        print("done.")
