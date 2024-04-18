from typing import NamedTuple
from typing import Optional
from setup_logging import setup_logging
from datetime import datetime
import logging
import os
from ssh_utils import * 

logger = logging.getLogger()

class Ssh_log(NamedTuple):
    date: Optional[datetime]
    serwer: Optional[str]
    sshd: Optional[str]
    message: Optional[str]


def read_logs(name:str) -> list[Ssh_log]:
    if not os.path.exists(name):
        logger.warning(f"File {name} does not exist")
        return None
    logs = []
    with open(name,"r") as file:
        for line in file:
            line = line.strip().split()
            date = get_date_from_log(line[0],line[1],line[2])
            message = get_message_from_log(line)
            if line and date and message:
                logs.append(Ssh_log(date, line[3], get_sshd_from_log(line[4]), message))
                ipv4 = get_ipv4s_from_log(Ssh_log(date, line[3], get_sshd_from_log(line[4]), message))
                if len(ipv4) > 1:
                    print(ipv4)
            else:
                logger.warning(f"Line {line} is not valid")
                
    return logs

if __name__ == "__main__":
    setup_logging()
    read_logs("SSH.log")
    
    