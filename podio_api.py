from pypodio2 import api
import json, random, string

with open('podio.json') as credential_data:
    data = json.load(credential_data)

c = api.OAuthClient(data["client_id"], 
data["client_secrets"], 
data["username"], 
data["password"])


spaceteam_members = c.Application.get_items(24519593)['items']
members_which_need_to_be_created = []

for member in spaceteam_members:
    if "null" in member["fields"][0]["values"][0]["value"]:
        members_which_need_to_be_created.append(member)

json_1 = {
    "fields":     
        {"216758721":4}
}
#print(json.dumps(members_which_need_to_be_created[0]["fields"][1]["values"][0]["value"]))

all = string.ascii_lowercase+string.ascii_uppercase + \
    string.digits+string.punctuation
password = "".join(random.sample(all, 16))
given_name = members_which_need_to_be_created[0]["fields"][1]["values"][0]["value"]
surname = members_which_need_to_be_created[0]["fields"][2]["values"][0]["value"]

userinfo = {'primaryEmail': given_name.lower()+'.'+surname.lower()+'@spaceteam.at',
            'name': {'givenName': given_name, 'familyName': surname},
            'password': password, }
print(userinfo)
#print(c.Item.update(members_which_need_to_be_created[0]["item_id"],json_1))
#print(members_which_need_to_be_created)