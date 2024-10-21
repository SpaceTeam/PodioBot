from flask import Flask, request
from manage_new_accounts import manage_new_accounts
from membership_handling import remind_members
import requests, threading, schedule, time

app = Flask(__name__)


@app.route("/")
def ok():
    return "Beep Boop, I'm the PodioBot 🤖"


@app.post("/")
def handle_hook():
    hook_data = request.form
    print(hook_data)
    if hook_data["type"] == "item.create":
        manage_new_accounts()
    elif hook_data["type"] == "hook.verify":
        podio = PodioAPI("podio.json")
        podio.validate_webhook(hook_id=hook_data["hook_id"], code=hook_data["code"])
    return "OK"


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    schedule.every(15).minutes.do(manage_new_accounts)
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    manage_new_accounts()

    app.run(host="0.0.0.0")
