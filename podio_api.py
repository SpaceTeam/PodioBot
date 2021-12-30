from pypodio2 import api
import json

with open('podio.json', 'r') as credential_data:
    data = json.load(credential_data)

c = api.OAuthClient(data["client_id"], 
data["client_secrets"], 
data["username"], 
data["password"])
print(c.Item.find(84))