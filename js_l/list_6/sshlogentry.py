from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from datetime import datetime
from typing import Optional
import re

class SSHLogEntry(ABC):
    def __init__(self,pid:int,raw_mess:str,time:datetime,user:str = None) -> None:
        
        self.regex = r"(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s\w+\s\w+\[([0-9]+)\]:\s(.*)"
        
        self.pid = pid
        self.time = time
        self.__raw_mess = raw_mess
        self.user = user
    
    def __str__(self) -> str:
        return f'{self.time}, {self.host_name}, {self.pid}'
    
    def getIPv4Address(self) -> Optional[IPv4Address]:
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",self.__raw_mess)
        if not ip:
            return None
        return IPv4Address(ip[0])
    
    def __repr__(self) -> str:
        return f'SSHLogEntry: {self.time}, {self.host_name}, {self.pid}'
    
    def __eq__(self, object) -> bool: 
        return self.time == object.time # and self.host_name == object.host_name and self.pid == object.pid
    
    def __lt__(self, value: object) -> bool: 
        return self.time < value.time
    
    def __gt__(self, value: object) -> bool: 
        return self.time > value.time
    
    
    @abstractmethod
    def validate(self) -> bool:
        pass
    
    @property
    def has_ip(self) -> bool: #TODO
        if self.getIPv4Address():
            return True
        return False
        
class SSHLogFailedPasswd(SSHLogEntry):
    def __init__(self,pid:int,raw_mess:str,time:datetime,ipv4:IPv4Address,port:int,user:str=None) -> None:
        super().__init__(pid,raw_mess,time,user)
        self.ipv4 = ipv4
        self.port = port 

    def validate(self) -> bool:
        match = re.match(self.regex, self.__raw_mess)
        
        if match:
            try:
                time = datetime.strptime(match.group(1), "%b %d %H:%M:%S")
                pid = int(match.group(2))
                message = match.group(3)
            except:
                return False
            
            if self.pid != pid:
                return False
            if self.time != time:
                return False
        
            patterns = [r" invalid user (\w+)", r'session opened for user (\w+)',r'session closed for user (\w+)', r'Accepted password for (\w+)',
                        r'Failed password for invalid user (\w+)']

            for pattern in patterns:
                matches = re.findall(pattern, message)
                if matches:
                    if self.user != matches[0]:
                        return False
            
            port = re.findall(r"port (\d+)",message)
            if not port:
                return False
            if int(port[0]) == self.port:
                return True

        return False

class SSHLogAcceptedPasswd(SSHLogEntry):
    def __init__(self,pid:int,raw_mess:str,time:datetime,ipv4:IPv4Address,port:int,user:str=None) -> None:
            super().__init__(pid,raw_mess,time,user)
            self.ipv4 = ipv4
            self.port = port 

    def validate(self) -> bool:
        match = re.match(self.regex, self.__raw_mess)
        
        if match:
            try:
                time = datetime.strptime(match.group(1), "%b %d %H:%M:%S")
                pid = int(match.group(2))
                message = match.group(3)
            except:
                return False
            
            if self.pid != pid:
                return False
            if self.time != time:
                return False
        
            patterns = [r" invalid user (\w+)", r'session opened for user (\w+)',r'session closed for user (\w+)', r'Accepted password for (\w+)',
                        r'Failed password for invalid user (\w+)']

            for pattern in patterns:
                matches = re.findall(pattern, message)
                if matches:
                    if self.user != matches[0]:
                        return False
            
            port = re.findall(r"port (\d+)",message)
            if not port:
                return False
            if int(port[0]) == self.port:
                return True

        return False
    
class SSHLogError(SSHLogEntry):
    def __init__(self,pid:int,raw_mess:str,time:datetime,error:int,user:str=None) -> None:
        super().__init__(pid,raw_mess,time,user)
        self.error        
    
    def validate(self) -> bool:
        match = re.match(self.regex, self.__raw_mess)
        
        if match:
            try:
                time = datetime.strptime(match.group(1), "%b %d %H:%M:%S")
                pid = int(match.group(2))
                message = match.group(3)
            except:
                return False
            
            if self.pid != pid:
                return False
            if self.time != time:
                return False
        
            error_pattern = r' \d+\: '
            error_match = re.findall(error_pattern, message)
            if error_match:
                if int(error_match[0]) == self.error:
                    return True
        return False
    
class SSHLogOther(SSHLogEntry):
    def __init__(self,pid:int,raw_mess:str,time:datetime,user:str=None) -> None:
        super().__init__(pid,raw_mess,time,user)
    
    def validate(self) -> bool:
        return True
    
