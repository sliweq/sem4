from typing import Generator
from sshlogentry import *


class SSHLogJournal():
    def __init__(self) -> None:
        self.logs = []
    
    def __len__(self) -> int:
        return len(self.logs)
    
    def __contains__(self, log : SSHLogEntry) -> bool:
        for l in self.logs:
            if log == l:
                return True
        return False
    
    def __iter__(self) -> Generator[SSHLogEntry,None,None]:
        for log in self.logs:
            yield log
    
    
    def append(self,log:str) -> bool: #TODO
        failed_passwd = [r'Failed password for invalid user (\w+)', r'Failed password for (\w+)']
        succesful_passwd = r'Accepted password for (\w+)'
        error = r']: error: '
        
        
        regex = r"(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s\w+\s\w+\[([0-9]+)\]:\s(.*)"
        match = re.match(regex, log)
        if match:
            try:
                time = datetime.strptime(match.group(1), "%b %d %H:%M:%S")
                pid = int(match.group(2))
                message = match.group(3)
            except:
                return False
        
        patterns = [r" invalid user (\w+)", r'session opened for user (\w+)',r'session closed for user (\w+)', r'Accepted password for (\w+)',r'Failed password for (\w+)']
        for pattern in patterns:
            matches = re.findall(pattern, message)
            if matches:
                user = matches[0]
        
        ports = re.findall(r"port (\d+) ssh2",message)
        
        if re.findall(failed_passwd,log):
            
            self.logs.append(SSHLogFailedPasswd(pid=pid,raw_mess=log,time=time,user=user,port=int(ports[0])))
            return True
        
        if re.findall(succesful_passwd,log):
            self.logs.append(SSHLogAcceptedPasswd(pid=pid,raw_mess=log,time=time,user=user,port=int(ports[0])))
            return True
        if re.findall(error,log):
            match = re.search(r'[^:]+$', log)
            if match:
                text_after_last_colon = match.group(0).strip()
                self.logs.append(SSHLogError(pid=pid,raw_mess=log,time=time,error=text_after_last_colon,user=user))
                return True
            
        
        self.logs.append(SSHLogEntry())
        return False

    def get_specified_logs(self,start_date:datetime, end_date:datetime, ip_v4 = None ) -> list[SSHLogEntry]:
        new_logs = []
        
        for log in self.logs:
            if log.time >= start_date and log.time <= end_date:
                if ip_v4:
                    if ip_v4 == log.ipv4:
                        new_logs.append(log)
                else:
                    new_logs.append(log)
        
        return new_logs
        