from dataclasses import dataclass

@dataclass
class User:
    email: str
    recovery_email: str
    given_name: str
    family_name: str
    password: str
    phonenumber: str | None
