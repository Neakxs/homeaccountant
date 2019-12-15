from dataclasses import dataclass

@dataclass
class User:
    email: str
    password_salt: str
    password_hash: str
    uid: int = None
    enabled: bool = False
    display_name: str = None