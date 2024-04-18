from datetime import datetime
import re
from typing import Optional
from setup_logging import setup_logging
from main import Ssh_log
from enum import Enum
import sys
import logging
# Dec 10 06:55:46 LabSZ sshd[24200]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!

logger = logging.getLogger()
setup_logging()

def get_date_from_log(month:str,day:str,time:str) -> Optional[datetime]:
    try:
        return datetime.strptime(f"{month} {day} {time}","%b %d %H:%M:%S")
    except ValueError:
        return None
    
def get_sshd_from_log(line:str) -> Optional[str]:
    try:
        return line.split("[")[1].split("]")[0]
    except IndexError:
        return None

def get_message_from_log(log:list[str]) -> Optional[str]:
    try:
        return " ".join(log[5:])
    except IndexError:
        return None
    
def get_ipv4s_from_log(log:Ssh_log) -> list[str]:
    # \d - digit
    # {1,3} - 1 to 3 times 
    # \. - dot
    return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",log.message) 

def get_user_from_message(log:Ssh_log) -> Optional[list[str]]:
    return names := re.findall(r"user (\w+)",log.message) if names else None
    # return list(map(lambda x: x.split()[1] ,re.findall(r"user (\w+)",log.message)))


class MessageType(Enum):
    SuccessfulLogin = 1
    FailedLogin = 2
    ClosedConnection = 3
    InvalidPassword = 4
    InvalidUser = 5
    HackAttempt = 6
    Other = 7 
    
def get_message_type(log:Ssh_log) -> MessageType:
    if "Accepted password for" in log.message:
        return MessageType.SuccessfulLogin
    if "authentication failure;" in log.message:
        return MessageType.FailedLogin
    if "Received disconnect from" in log.message:
        return MessageType.ClosedConnection
    if re.findall(r"Failed password for (\S+) from",log.message):
        return MessageType.InvalidPassword
    if "Invalid user" in log.message:
        return MessageType.InvalidUser
    if "POSSIBLE BREAK-IN ATTEMPT" in log.message:
        return MessageType.HackAttempt
    
    return MessageType.Other

def report_log(log:Ssh_log) -> None:
    log_type = get_message_type(log)
    
    
            