from dataclasses import dataclass

@dataclass
class User:
    email: str = None
    password_salt: str = None
    password_hash: str = None
    uid: int = None
    enabled: bool = False
    display_name: str = None