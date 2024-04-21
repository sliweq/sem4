from typing import NamedTuple
from typing import Optional
from datetime import datetime
from enum import Enum

class Ssh_log(NamedTuple):
    date: Optional[datetime]
    serwer: Optional[str]
    sshd: Optional[str]
    message: Optional[str]
    
class MessageType(Enum):
    SuccessfulLogin = 1
    FailedLogin = 2
    ClosedConnection = 3
    InvalidPassword = 4
    InvalidUser = 5
    HackAttempt = 6
    Other = 7 

class Shh_session(NamedTuple):
    start: list[Ssh_log] 
    close: list[Ssh_log]