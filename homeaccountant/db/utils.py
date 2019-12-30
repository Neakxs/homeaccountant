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
    balance: int
    acronym: str
    user: User = None
    uid: int = None

@dataclass
class TransactionFamily:
    uid: int = None
    name: str = None


@dataclass
class TransactionCategory:
    uid: int = None
    name: str = None
    user: User = None
    family: TransactionFamily = None
