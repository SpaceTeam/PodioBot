from pypodio2 import api
import json

class PodioAPI:
    def __init__(self, config_name: str):
        with open(config_name) as credential_data:
            data = json.load(credential_data)

        self.c = api.OAuthClient(data["client_id"], 
            data["client_secrets"], 
            data["username"], 
            data["password"])


    def get_new_members(self) -> list:

        spaceteam_members = self.c.Application.get_items(24519593)['items']
        members_which_need_to_be_created = []

        for member in spaceteam_members:
            if "null" in member["fields"][0]["values"][0]["value"]:
                members_which_need_to_be_created.append(member)
        return members_which_need_to_be_created


#print(json.dumps(members_which_need_to_be_created[0]["fields"][1]["values"][0]["value"]))

    def change_state_of_member(self, id: int, state: int): # 4 = in arbeit #members_which_need_to_be_created[0]["item_id"]
        self.c.Item.update(id,{
            "fields":     
                    {"216758721":state}
        })




#json_1 = {
#    "fields":     
#        {"216758721":4}
#}
#print(c.Item.update(members_which_need_to_be_created[0]["item_id"],json_1))
#print(members_which_need_to_be_created)