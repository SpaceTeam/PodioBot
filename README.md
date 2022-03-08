# PodioBot
A simple bot to automate the creation of the accounts for new 
[Space Team](https://spaceteam.at/) members.


## Features
* Pull new users from podio
* Create a google workspace account with a random password
* Send the new member a welcome email (with their new spaceteam eamil)


## Usage
Before you start rename all `*.json.example` files to `.json` files and edit the
configuration in them.

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3.10 main.py
```

<!--
## Deploy 
We deploy this bot as a systemd service on Ubuntu 2020.

First, install python with:
-->
