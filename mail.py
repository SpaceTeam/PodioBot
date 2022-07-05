from email.mime.multipart import MIMEMultipart

import smtplib, json
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Environment, select_autoescape, FileSystemLoader
from datetime import date

from user import User


def current_semester() -> str:
    today = date.today()
    msg = str(today.year)

    if today.month < 6:
        msg += "S"
    else:
        msg += "W"
    
    return msg


class MailSender:
    def __init__(self, config_file: str) -> None:
        with open(config_file) as mail_data:
            self.config = json.load(mail_data)

        self.env = Environment(
            loader=FileSystemLoader("."),
            autoescape=select_autoescape(["html", "xml"]),
        )
        
    def send_reminder_email(self, user: User) -> None:
        template = self.env.get_template(self.config["reminder_template"])
        msg = MIMEMultipart()

        body = template.render(user=user)

        msg.attach(MIMEText(body, "html"))

        # enconding the binary into base64

        msg["Subject"] = "Beitragserinnerung TU Space Team - Membershipfee reminder TU Space Team"
        msg["From"] = self.config["username"]
        msg["To"] = user.recovery_email

        with smtplib.SMTP(self.config["domain"], self.config["port"]) as server:
            #server.starttls()
            #server.ehlo()
            #server.login(self.config["username"], self.config["password"])
            #server.sendmail(
            #    self.config["username"], [user.recovery_email], msg.as_string()
            #)
            print("Successfully sent email.")






    def send_welcome_mail(self, user: User) -> None:
        template = self.env.get_template(self.config["welcome_template"])
        msg = MIMEMultipart()

        body = template.render(user=user, current_semester=current_semester())

        msg.attach(MIMEText(body, "html"))
        binary_pdf = open(self.config["pdf"], "rb")

        payload = MIMEBase("application", "octate-stream", Name=self.config["pdf"])
        # payload = MIMEBase('application', 'pdf', Name=pdfname)
        payload.set_payload((binary_pdf).read())

        # enconding the binary into base64
        encoders.encode_base64(payload)

        # add header with pdf name
        payload.add_header(
            "Content-Decomposition", "attachment", filename=self.config["pdf"]
        )
        msg.attach(payload)

        msg["Subject"] = "Willkommen im TU Space Team - Welcome to TU Space Team"
        msg["From"] = self.config["username"]
        msg["To"] = user.recovery_email

        with smtplib.SMTP(self.config["domain"], self.config["port"]) as server:
            server.starttls()
            server.ehlo()
            server.login(self.config["username"], self.config["password"])
            server.sendmail(
                self.config["username"], [user.recovery_email], msg.as_string()
            )
            print("Successfully sent email.")
