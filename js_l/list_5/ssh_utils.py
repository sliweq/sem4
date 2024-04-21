from datetime import datetime
import re
from typing import Optional
from setup_logging import setup_logging
from main import Ssh_log
from ssh_class import MessageType, Shh_session
import logging
import statistics
import argparse
from main import LOG_LEVEL

logger = logging.getLogger()
setup_logging(LOG_LEVEL)

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
    # zadanie 2 b
    return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",log.message) 

def get_user_from_message(log:Ssh_log) -> Optional[str]:
    # zadanie 2 c
    names = re.findall(r" user (\w+)",log.message) 
    if names: 
        if names[0] != "unknown":
            return names[0]
    return None

def get_all_users(logs:list[Ssh_log]) -> list[str]:
    users = []
    for log in logs:
        user = get_user_from_message(log)
        if user and user not in users:
            users.append(user)
    return users

def draw_users(users:list[str]) -> Optional[str]:
    import random
    return random.choice(users)

def get_message_type(log:Ssh_log) -> MessageType:
    # zadanie 2 d
    if "Accepted password for" in log.message:
        return MessageType.SuccessfulLogin
    if "authentication failure;" in log.message:
        return MessageType.FailedLogin
    if "Received disconnect from" in log.message or "Connection closed by" in log.message:
        return MessageType.ClosedConnection
    if re.findall(r"Failed password for (\S+) from",log.message):
        return MessageType.InvalidPassword
    if "Invalid user" in log.message:
        return MessageType.InvalidUser
    if "POSSIBLE BREAK-IN ATTEMPT" in log.message:
        return MessageType.HackAttempt
    
    return MessageType.Other

def report_log(log:Ssh_log) -> None:
    match get_message_type(log):
        case MessageType.SuccessfulLogin:
            logger.info(f"Successful login")
        case MessageType.FailedLogin:
            logger.warning(f"Failed login ")
        case MessageType.ClosedConnection:
            logger.info(f"Connection closed")
        case MessageType.InvalidPassword:
            logger.warning(f"Invalid password")
        case MessageType.InvalidUser:
            logger.warning(f"Invalid user")
        case MessageType.HackAttempt:
            logger.error(f"Hack attempt")
        case MessageType.Other:
            logger.debug(f"Other message")
        
def read_bytes(line:str) -> None:
    logger.debug(f"Read {len(line)} bytes")
    
def get_sessions(logs:list[Ssh_log]) -> Shh_session:
    start = []
    close = []
    for log in logs:
        if " session opened " in log.message:
            start.append(log)
        if " session closed " in log.message:
            close.append(log)
    return Shh_session(start=start,close=close)

def user_session_time(user:str, session:Shh_session) -> list[float]:
    time = []
    for log in session.start:
        if get_user_from_message(log) == user:
            start = log.date
            for log in session.close:
                if get_user_from_message(log) == user:
                    if log.date >= start:
                        time.append((log.date - start).total_seconds())
                        break
    return time
                    
def all_users_session_time(sessions:Shh_session) -> list[float]:
    time = []
    for log in sessions.start:
        user = get_user_from_message(log)
        if not user:
            continue
        start = log.date
        for log in sessions.close:
                if get_user_from_message(log) == user:
                    if log.date >= start:
                        time.append((log.date - start).total_seconds())
                        break
    return time

def extract_users_from_sessions(sessions:Shh_session) -> list[str]:
    users = []
    for log in sessions.start:
        user = get_user_from_message(log)
        users.append(user)
    return users

def get_n_logs(logs:list[Ssh_log],n:int) -> None:
    # zadanie 4 a
    users = get_all_users(logs)
    if not users:
        logger.warning("No users found")
        return 
    chosen_user = draw_users(users)
    if not chosen_user:
        logger.warning("No user chosen")
        return 
    logs = [log for log in logs if get_user_from_message(log) == chosen_user]
    if not logs:
        logger.warning("No logs found")
        return 
    print(f"User {chosen_user} logs")
    if len(logs) < n:
        for log in logs:
            print(log.message)
        return
    import random
    for log in range(n):
        print(random.choice(logs).message)
    
def average_connection_time(logs:list[Ssh_log]) -> None:
    sessions = get_sessions(logs)
    if not sessions:
        logger.warning("No sessions found")
        return
    users = get_all_users(logs)
    
    for user in users:
        user_session = user_session_time(user,sessions)
        if not user_session:
            # logger.warning(f"No sessions found for user {user}")
            continue
        if len(user_session) == 1:
            print(f"{user}: avg: {round(statistics.mean(user_session),2)}")
        else:    
            print(f"{user}: avg: {round(statistics.mean(user_session),2)} stddev: {round(statistics.stdev(user_session),2)}")
    all_user_sessions = all_users_session_time(sessions)
    if not all_user_sessions:
        logger.warning("No sessions found")
        return
    print(f"Total: avg: {round(statistics.mean(all_user_sessions),2)} stddev: {round(statistics.stdev(all_user_sessions),2)}")

def get_most_less_active_user(logs:list[Ssh_log]) -> None:
    sessions = get_sessions(logs)
    if not sessions:
        logger.warning("No sessions found")
        return ""
    tmp = extract_users_from_sessions(sessions)
    print(f"Most active user: {max(set(tmp), key = tmp.count)}")
    print(f"Least active user: {min(set(tmp), key = tmp.count)}")