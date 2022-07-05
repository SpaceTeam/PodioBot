
from podio_api import PodioAPI
from misc import gen_random_password
from user import User
from mail import MailSender
from ascii import translate_to_ascii
from datetime import datetime
import json

def remind_members():
    podio = PodioAPI('podio.json')
    mail_sender = MailSender('mail.json')
    
    #print("Fetching members from podio ...")
    all_members = podio.get_all_members()
    #print("done.")
    
    if len(all_members) == 0:
        print("No members found. Major ERROR")
        exit()

    current_time = datetime.now()

    members_which_need_to_be_reminded = []
    print(f"Got {len(all_members)} members.")

    for member in all_members:
        payed_until = datetime.strptime(podio.get_start_of_field_with_id(229789505, member), "%Y-%m-%d %H:%M:%S")
        if (current_time < payed_until):
            #print("payed.")
        else:
            members_which_need_to_be_reminded.append(member)

    print(f"Sending {len(members_which_need_to_be_reminded)} reminders.")
    for member in members_which_need_to_be_reminded:
        print("Sending mail reminder ...")
        given_name = podio.get_value_of_field_with_id(206982183,member)
        surname = podio.get_value_of_field_with_id(206982184,member)
        recovery_email = podio.get_value_of_field_with_id(206982186,member)
        podio_id = member["item_id"]
        
        user = User(
            email=translate_to_ascii(given_name.lower()+'.'+surname.lower())+'@spaceteam.at',
            recovery_email=recovery_email,
            given_name = given_name,
            family_name = surname,
            password="",
        )
        mail_sender.send_reminder_email(user);
        print("done.")
    exit()
        #mail_sender.send_welcome_mail(user)
   
        #print("Updating begin of membership ...")
        #print(podio.update_begin_of_membership(podio_id))
        #print("done.")