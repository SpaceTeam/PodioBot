from pypodio2 import api
import json

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

json = {
    "fields":     
        {"216758721":4}
}
print(c.Item.update(members_which_need_to_be_created[0]["item_id"],json))
#print(members_which_need_to_be_created)