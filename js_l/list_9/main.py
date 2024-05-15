from ipaddress import IPv4Address
from sshuser import SSHUser
from datetime import datetime
from sshlogentry import SSHLogEntry
from sshlogjournal import SSHLogJournal
from typing import Union, cast, Any, List

journalctl = SSHLogJournal()

with open('SSH.log', 'r') as f:
    lines = f.readlines()
    for line in lines[:1000]:
        journalctl.append(line.strip())
        
        
print(len(journalctl))

start = datetime.strptime('Dec 10 07:18:31', "%b %d %H:%M:%S")
end = datetime.strptime('Dec 10 07:27:54', "%b %d %H:%M:%S")

for log in journalctl.get_specified_logs(start, end):
    print(log)

print(journalctl[0])
print(journalctl[1:10])

tmp: List[Any] = journalctl[IPv4Address('173.234.31.186')]
#tmp: List[Union[SSHLogEntry, SSHUser]] = cast(List[Union[SSHLogEntry, SSHUser]], journalctl[IPv4Address('173.234.31.186')])
# Sequence[Union[SSHLogEntry, SSHUser]] 

for t in tmp:
    print(t.validate())
    
tmp.append(SSHUser("test",datetime.now()))
 
for t in tmp:
    print(t.validate())