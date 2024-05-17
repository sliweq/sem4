from sshlogentry import *
from datetime import datetime
import pytest
from ipaddress import IPv4Address
from typing import Optional
from sshlogjournal import SSHLogJournal

@pytest.mark.parametrize("input, expected", [
    (SSHLogFailedPasswd(pid = 24200, raw_mess ="Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2",
                    time = datetime.strptime('Dec 10 06:55:48', "%b %d %H:%M:%S"), ipv4 = IPv4Address('173.234.31.186'), port = 38926),
     datetime.strptime('Dec 10 06:55:48', "%b %d %H:%M:%S")),        
    (SSHLogFailedPasswd(pid = 24200, raw_mess ="Xd 40 12:22:11 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2",
                    time = datetime.strptime('Dec 10 06:55:41', "%b %d %H:%M:%S"), ipv4 = IPv4Address('173.234.31.186'), port = 38926),None), 
    (SSHLogFailedPasswd(pid = 24200, raw_mess ="Dec 12 12:100:11 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2",
                    time = datetime.strptime('Dec 10 06:55:41', "%b %d %H:%M:%S"), ipv4 = IPv4Address('173.234.31.186'), port = 38926),None), 
])
def test_datetime(input : SSHLogFailedPasswd, expected:Optional[datetime]) -> None:
    assert input.getDateTime() == expected
    
@pytest.mark.parametrize("input, expected", [
    (SSHLogFailedPasswd(pid = 24200, raw_mess ="Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 666.777.88.213 port 38926 ssh2",
                        time = datetime.strptime('Dec 10 06:55:48', "%b %d %H:%M:%S"), ipv4 = IPv4Address('173.234.31.186'), port = 38926),None),
    (SSHLogFailedPasswd(pid = 24200, raw_mess ="Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2",
                        time = datetime.strptime('Dec 10 06:55:48', "%b %d %H:%M:%S"), ipv4 = IPv4Address('173.234.31.186'), port = 38926),IPv4Address('173.234.31.186')),
    (SSHLogError(pid =24324, raw_mess="Dec 10 07:51:15 LabSZ sshd[24324]: error: Received disconnect from : 3: com.jcraft.jsch.JSchException: Auth fail [preauth]",
                        time=datetime.strptime('Dec 10 07:51:15', "%b %d %H:%M:%S"),error=3),None)
    ])
def test_ipv4(input: SSHLogEntry, expected:Optional[datetime]) -> None:
    assert input.getIPv4Address() == expected

@pytest.mark.parametrize("input, expected", [
    ("Dec 10 09:11:34 LabSZ sshd[24447]: Failed password for invalid user 1234 from 103.99.0.122 port 53950 ssh2", SSHLogFailedPasswd),
    ("Dec 10 09:11:34 LabSZ sshd[24447]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]", SSHLogError),
    ("Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for fztu from 119.137.62.142 port 49116 ssh2" , SSHLogAcceptedPasswd),
    ("Dec 10 09:32:35 LabSZ sshd[24787]: pam_unix(sshd:auth): check pass; user unknown",SSHLogOther)
    
])
def test_append(input:str, expected:type) -> None:
    joutnal = SSHLogJournal()
    joutnal.append(input)
    try:
        
        assert isinstance(joutnal[0][0],expected)
    except IndexError:
        assert False
    
