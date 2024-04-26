from abc import ABC
from ipaddress import IPv4Address
from datetime import datetime
from typing import Optional
import re

regex = r"(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s\w+\s\w+\[([0-9]+)\]:\s(.*)"



class SSHLogEntry(ABC):
    def __init__(self,log:str) -> None:
        self.log = log
        self.regex = r"(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s\w+\s\w+\[([0-9]+)\]:\s(.*)"
        
        self.pid = None
        self.time = None
        self.message = None
        
        match = re.match(regex, log)
        if match:
            self.time = datetime.strptime(match.group(1), "%b %d %H:%M:%S")
            self.pid = int(match.group(2))
            self.message = match.group(3)
    
    def __str__(self) -> str:
        # return f'{self.time} {self.host_name} {self.pid} {self.message}'
        pass 
    
    def getIPv4Address(self) -> Optional[IPv4Address]:
        pass
        # return None
        
class SSHLogFailedPasswd(SSHLogEntry):
    ...

class SSHLogAcceptedPasswd(SSHLogEntry):
    ...

class SSHLogError(SSHLogEntry):
    ...
    
class SSHLogOther(SSHLogEntry):
    ...
