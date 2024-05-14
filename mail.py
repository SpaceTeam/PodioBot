from email.mime.multipart import MIMEMultipart

import smtplib, json
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from jinja2 import Environment, select_autoescape, FileSystemLoader
from datetime import date

from qr import generateQRCode
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

    def send_mail(self, msg: MIMEMultipart, email: str):
        msg.add_header("reply-to", "hr@spaceteam.at")
        with smtplib.SMTP(self.config["domain"], self.config["port"]) as server:
            server.starttls()
            server.ehlo()
            server.login(self.config["username"], self.config["password"])
            server.sendmail(self.config["username"], [email], msg.as_string())
            print("Successfully sent email.")

    def send_plain_email(self, subject: str, message: str, email: str):
        msg = MIMEMultipart()
        msg.attach(MIMEText(message, "plain"))

        msg["Subject"] = subject
        msg["From"] = self.config["username"]
        msg["To"] = email
        self.send_mail(msg, email)

    def send_reminder_email(self, user: User, amount: int, days_not_payed: int) -> None:
        templates_config = self.config["reminder_template"]
        template = None
        for key in sorted(templates_config.keys(), reverse=True):
            if int(key) <= days_not_payed:
                template = templates_config[key]
                break
        if template is None:
            print(
                "Did not send email for",
                user.given_name,
                user.family_name,
                "because",
                days_not_payed,
                "days did not match a template.",
            )
            return

        template = self.env.get_template(template)
        signature = self.env.get_template(self.config["signature_template"])
        sig_body = signature.render()
        body = template.render(
            user=user, amount=amount, days_not_payed=days_not_payed, signature=sig_body
        )

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "html"))
        msg[
            "Subject"
        ] = "Beitragserinnerung TU Space Team - Membershipfee reminder TU Space Team"
        msg["From"] = self.config["username"]
        msg["To"] = user.recovery_email
        image = MIMEImage(
            generateQRCode(
                recipient=self.config["banking_account_name"],
                iban=self.config["iban"],
                amount=amount,
                currency=self.config["currency"],
                purpose=f"MGB {user.given_name} {user.family_name}",
            )
        )
        image.add_header("Content-Disposition", "attachment", filename="qrcode.png")
        msg.attach(image)
        self.send_mail(msg, user.recovery_email)

    def send_welcome_mail(self, user: User) -> None:
        template = self.env.get_template(self.config["welcome_template"])
        msg = MIMEMultipart()

        body = template.render(user=user, current_semester=current_semester())

        msg.attach(MIMEText(body, "html"))
        # binary_pdf = open(self.config["pdf"], "rb")

        # payload = MIMEBase("application", "octate-stream", Name=self.config["pdf"])
        # payload.set_payload((binary_pdf).read())

        # TODO: Doesn't work in all email clients
        # enconding the binary into base64
        # encoders.encode_base64(payload)

        # add header with pdf name
        # payload.add_header(
        #    "Content-Decomposition", "attachment", filename=self.config["pdf"]
        # )
        # msg.attach(payload)

        msg["Subject"] = "Willkommen im TU Space Team - Welcome to TU Space Team"
        msg["From"] = self.config["username"]
        msg["To"] = user.recovery_email

        self.send_mail(msg, user.recovery_email)


if __name__ == "__main__":
    # sending test email
    mail_handler = MailSender("mail.json")
    user = User(
        email="paul.hoeller@spaceteam.at",
        recovery_email="paul.hoeller@spaceteam.at",
        given_name="Paul",
        family_name="Höller",
        password="",
    )
    user2 = User(
        email="alicia.wollendorfer@spaceteam.at",
        recovery_email="alicia.wollendorfer@spaceteam.at",
        given_name="Alicia",
        family_name="Wollendorfer",
        password="",
    )
    user3 = User(
        email="patrick.kappl@spaceteam.at",
        recovery_email="patrick.kappl@spaceteam.at",
        given_name="Patrick",
        family_name="Kappl",
        password="",
    )
    mail_handler.send_welcome_mail(user=user)
    # mail_handler.send_reminder_email(user=user2, amount=25, days_not_payed=31)
    # mail_handler.send_reminder_email(user=user2, amount=25, days_not_payed=61)
    # mail_handler.send_reminder_email(user=user2, amount=25, days_not_payed=91)
    # mail_handler.send_plain_email("Test Email", "Test email to see if smtp is correctly set up", "it@spaceteam.at")
