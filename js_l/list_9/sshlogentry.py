from abc import ABC, abstractmethod
from ipaddress import IPv4Address, AddressValueError
from datetime import datetime
from typing import Any, Optional
import re

class SSHLogEntry(ABC):
    def __init__(self,pid:int,raw_mess:str,time:datetime,user:Optional[str] = None) -> None:
        
        self.regex = r"(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s\w+\s\w+\[([0-9]+)\]:\s(.*)"
        
        self.pid = pid
        self.time = time
        self._raw_mess = raw_mess
        self.user = user
        self.ipv4 : Optional[IPv4Address] = None
    
    def __str__(self) -> str:
        if self.user:
            return f'{self.time}, {self.user}, {self.pid}'
        return f'{self.time}, {self.pid}'
    
    def getIPv4Address(self) -> Optional[IPv4Address]:
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",self._raw_mess)
        if not ip:
            return None
        try:
            return IPv4Address(ip[0])
        except AddressValueError:
            return None
    
    def getDateTime(self) -> Optional[datetime]:
        time_in_raw = re.findall(r"(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})",self._raw_mess)
        if not time_in_raw:
            return None
        try:
            new_time = datetime.strptime(time_in_raw[0], "%b %d %H:%M:%S")
            return new_time
        except (IndexError, ValueError):
            return None
        
    
    def __repr__(self) -> str:
        if self.user:
            return f'SSHLogEntry: {self.time}, {self.user}, {self.pid}, {self._raw_mess}'
        return f'SSHLogEntry: {self.time}, {self.pid}, {self._raw_mess}'
    
    def __eq__(self, object : Any) -> bool: 
        if not isinstance(object, SSHLogEntry):
            return False
        return self.time == object.time # and self.user == object.user and self.pid == object.pid
    
    def __lt__(self, value: 'SSHLogEntry') -> bool: 
        return self.time < value.time 
    
    def __gt__(self, value: 'SSHLogEntry') -> bool: 
        return self.time > value.time
    
    
    @abstractmethod
    def validate(self) -> bool:
        pass
    
    @property
    def has_ip(self) -> bool:
        if self.getIPv4Address():
            return True
        return False
        
class SSHLogFailedPasswd(SSHLogEntry):
    def __init__(self,pid:int,raw_mess:str,time:datetime,ipv4:IPv4Address,port:int,user:Optional[str]=None) -> None:
        super().__init__(pid,raw_mess,time,user)
        self.ipv4 = ipv4
        self.port = port 

    def validate(self) -> bool:
        print(self._raw_mess)
        match = re.match(self.regex, self._raw_mess)
        
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
                        print(self.user, matches[0])
                        return False
            
            port = re.findall(r"port (\d+)",message)
            if not port:
                return False
            if int(port[0]) == self.port:
                return True

        return False

class SSHLogAcceptedPasswd(SSHLogEntry):
    def __init__(self,pid:int,raw_mess:str,time:datetime,ipv4:IPv4Address,port:int,user:Optional[str]=None) -> None:
            super().__init__(pid,raw_mess,time,user)
            self.ipv4 = ipv4
            self.port = port 

    def validate(self) -> bool:
        match = re.match(self.regex, self._raw_mess)
        
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
    def __init__(self,pid:int,raw_mess:str,time:datetime,error:int,user:Optional[str]=None) -> None:
        super().__init__(pid,raw_mess,time,user)
        self.error = error   
    
    def validate(self) -> bool:
        match = re.match(self.regex, self._raw_mess)
        
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
    def __init__(self,pid:int,raw_mess:str,time:datetime,user:Optional[str]=None) -> None:
        super().__init__(pid,raw_mess,time,user)
    
    def validate(self) -> bool:
        return True
    
