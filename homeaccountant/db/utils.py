from dataclasses import dataclass

@dataclass
class User:
    email: str = None
    password_salt: str = None
    password_hash: str = None
    uid: int = None
    enabled: bool = False
    display_name: str = None

@dataclass
class Account:
    name: str
    summary: str
    acronym: str
    user: User = None
    uid: int = None

@dataclass
class TransactionFamily:
    name: str
    uid: int = None


@dataclass
class TransactionCategory:
    name: str
    user: User
    family: TransactionFamily
    uid: int = None
