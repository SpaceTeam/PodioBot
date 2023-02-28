# PodioBot
A simple bot to automate the creation of the accounts for new 
[Space Team](https://spaceteam.at/) members.


## Features
* Pull new users from podio
* Create a google workspace account with a random password
* Send the new member a welcome email (with their new spaceteam eamil)
* Remind members every month about unpaid meber fees with different templates


## Usage
Before you start rename all `*.json.example` files to `.json` files and edit the 
configuration in them. After that create all necessary template files. 

Available attributes in mail templates (none available in the signature file): 
* {{amount}}
* {{days_not_payed}}
* {{signature}}
* {{user.given_name}}
* {{user.family_name}}

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
