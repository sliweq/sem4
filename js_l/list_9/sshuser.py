from datetime import datetime
import re

class SSHUser():
    def __init__(self, username:str,lastlogin:datetime) -> None:
        self.username = username
        self.lastlogin = lastlogin
        
    def validate(self) -> bool:
        return re.compile(r'^[a-z_][a-z0-9_-]{0,31}$').match(self.username) is not None

    def __repr__(self) -> str:
        return f"User {self.username}, last seen {self.lastlogin}\n"