from podio_api import PodioAPI
from misc import gen_random_password
from user import User
from mail import MailSender
from ascii import translate_to_ascii
from datetime import datetime
import json, math

# Sends reminder email to members that haven't paid their membership fee.
def remind_members():
    podio = PodioAPI("podio.json")
    mail_sender = MailSender("mail.json")

    print("Fetching members from podio ...")
    all_members = podio.get_all_members()
    print("done.")

    print(f"Got {len(all_members)} members.")

    if len(all_members) == 0:
        print("No members found. Major ERROR")
        return 

    current_time = datetime.now()

    members_which_need_to_be_reminded = []

    statistics = {
        "members": 0,
        "total": 0,
        "high_payers": []
    }
    for member in all_members:
        payed_until = datetime.strptime(
            podio.get_start_of_field_with_id(229789505, member), "%Y-%m-%d %H:%M:%S"
        )
        if not current_time <= payed_until:
            amount = math.ceil((current_time-payed_until).days/(6*30))*25
            print(f"{(current_time-payed_until).days} days not payed for {podio.get_value_of_field_with_id(206982184, member)} = {amount}€")
            member.update({"amount":amount})
            members_which_need_to_be_reminded.append(member)

            given_name = podio.get_value_of_field_with_id(206982183, member)
            surname = podio.get_value_of_field_with_id(206982184, member)
            statistics["members"] += 1
            statistics["total"] += amount
            if amount > 100:
                statistics["high_payers"].append((given_name + " " + surname, amount))
    
    statistics["high_payers"].sort(key=lambda p: p[1])
    statistc_msg = f"{statistics['members']} received a membership payment reminder, tottalling in about €{statistics['total']}.\n"
    if len(statistics["high_payers"]) == 0:
        statistc_msg += "There are no worrisome members \(^.^)/"
    else: 
        statistc_msg += "The most worrisome members are:\n"
        statistc_msg += "".join(map(lambda hp: f"* {hp[0]}: {hp[1]}\n", statistics["high_payers"]))

    mail_sender.send_plain_email("Member reminder statistics", statistc_msg, "paul.hoeller@spaceteam.at")

    print(f"Sending {len(members_which_need_to_be_reminded)} reminders.")
    for member in members_which_need_to_be_reminded:
        if member is None:
            continue
        given_name = podio.get_value_of_field_with_id(206982183, member)
        surname = podio.get_value_of_field_with_id(206982184, member)
        recovery_email = podio.get_value_of_field_with_id(206982186, member)
        podio_id = member["item_id"]

        print(f"Sending mail reminder ({given_name} {surname}) ...")

        user = User(
            email=translate_to_ascii(given_name.lower() + "." + surname.lower())
            + "@spaceteam.at",
            recovery_email=recovery_email,
            given_name=given_name,
            family_name=surname,
            password="",
        )
        mail_sender.send_reminder_email(user,member["amount"])
        print("done.")