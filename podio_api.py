from pypodio2 import api
import json
from datetime import datetime

from user import User


class PodioAPI:
    def __init__(self, config_name: str):
        with open(config_name) as credential_data:
            data = json.load(credential_data)

        self.c = api.OAuthClient(
            data["client_id"],
            data["client_secrets"],
            data["username"],
            data["password"],
        )

    def get_new_members(self) -> list:

        spaceteam_members = self.c.Application.get_items(24519593)["items"]
        members_which_need_to_be_created = []

        for member in spaceteam_members:
            if "null" in member["fields"][0]["values"][0]["value"]:
                members_which_need_to_be_created.append(member)
        return members_which_need_to_be_created

    def get_all_members(self) -> list:
        count = self.c.Application.get_items("24519593/count")["count"]
        results = []
        for i in range(0, int(count / 30) + 1):
            result = self.c.Item.filter(
                24519593, attributes={"limit": 30, "offset": i * 30}
            )
            if "items" in result: 
                for item in result["items"]:
                    for field in item["fields"]:
                        if field["field_id"] ==  216758721 and "value" in field["values"][0] and "text" in field["values"][0]["value"] and field["values"][0]["value"]["text"] != "Ausgetreten": 
                            results.append(item)
                            break
        return results

    def validate_webhook(self, hook_id: int, code: int):
        self.c.Hook.validate(hook_id, code)

    def change_state_of_member(self, id: int, state: int):  
        # 4 = in arbeit #members_which_need_to_be_created[0]["item_id"]
        self.c.Item.update(id, {"fields": {"216758721": state}})

    def update_begin_of_membership(self, id: int):
        now = datetime.now()
        format = "%Y-%m-%d %H:%M:%S"
        time1 = now.strftime(format)
        self.c.Item.update(id, {"fields": {"229611689": {"start": time1}}})

    def update_st_email(self, id: int, user: User):
        self.c.Item.update(
            id, {"fields": {"216757856": {"type": "work", "value": user.email}}}
        )

    def get_value_of_field_with_id(self, id: int, items: list) -> str:
        for item in items["fields"]:
            if item["field_id"] == id:
                return item["values"][0]["value"]
        return None

    def get_start_of_field_with_id(self, id: int, items: list) -> str:
        for item in items["fields"]:
            if item["field_id"] == id:
                return item["values"][0]["start"]
        return None
