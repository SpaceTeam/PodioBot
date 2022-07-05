from flask import Flask, request
from manage_new_accounts import manage_new_accounts
from membership_handling import remind_members
import requests

app = Flask(__name__)


@app.route('/')
def ok():
    return 'OK'

@app.post('/')
def handle_hook():
    hook_data = request.form
    if hook_data['type'] == 'item.create':
        manage_new_accounts()
    elif hook_data['type'] == 'hook.verify':
        podio = PodioAPI('podio.json')
        podio.validate_webhook(hook_id=hook_data['hook_id'], code=hook_data['code'])
    return 'OK'

if __name__ == '__main__':
    manage_new_accounts()
    #remind_members()
    app.run(host="0.0.0.0")
    
