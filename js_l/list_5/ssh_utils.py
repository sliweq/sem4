from queue import Queue
from main import LOG_LEVEL
from datetime import datetime
import re
from typing import Optional
from setup_logging import setup_logging
from main import Ssh_log
from ssh_class import MessageType, Shh_session
import logging
import statistics

logger = logging.getLogger()
setup_logging(LOG_LEVEL)

def get_date_from_log(month:str) -> Optional[datetime]:
    try:
        return datetime.strptime(f"{month}","%b %d %H:%M:%S")
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
    patterns = [r" invalid user",r'Failed password for invalid user (\w+)', r'session opened for user (\w+)','session closed for user (\w+)']
    for pattern in patterns:
        matches = re.findall(pattern, log.message)
        if matches:
            return matches[0]
            
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
    
    if re.search("Accepted password for", log.message):
        return MessageType.SuccessfulLogin
    if re.search("authentication failure;", log.message):
        return MessageType.FailedLogin
    if re.search("Received disconnect from", log.message) or re.search("Connection closed by",log.message):
        return MessageType.ClosedConnection
    if re.findall(r"Failed password for (\S+) from",log.message):        
        return MessageType.InvalidPassword
    if re.search("Invalid user", log.message):
        return MessageType.InvalidUser
    if re.search("POSSIBLE BREAK-IN ATTEMPT", log.message):
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
    
    
def get_sessions(logs:list[Ssh_log]) -> Shh_session:
    start = []
    close = []
    for log in logs:
        
        if re.search(" session opened ", log.message):
            start.append(log)
        if re.search(" session closed ", log.message):
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
    
    
    
# brute force

class BruteForce():
    def __init__(self, logs:list[Ssh_log], duration:int = 100, user:str = None):
        self.logs = logs
        self.duration = duration
        self.user = user
        
        self.attacs = {} 
        self.potential_attacks = {}
        
        self.duration = duration
    
    def run(self) -> list[str]:
        if self.user:
            self.run_for_user()
        else:
            self.run_for_all()
        
        attacks = []
        
        for key,values in self.attacs.items():
            if values:
                attack = values[0]
                attack_index = 0
                tmp = 0
                while tmp < len(values):
                    if (values[tmp].date - attack.date).total_seconds() >= self.duration:
                        attacks.append(f"Attack from {key}, {tmp - attack_index+1} times, attack lasted for: {(values[tmp].date-attack.date).total_seconds()}")
                        attack = values[tmp]
                        attack_index = tmp
                    tmp += 1
        return attacks
    
    def add_log_to_dict(self,log:Ssh_log) -> None:

        if get_ipv4s_from_log(log)[0] not in self.potential_attacks.keys():
            self.potential_attacks[get_ipv4s_from_log(log)[0]] = Queue()
            
        self.potential_attacks[get_ipv4s_from_log(log)[0]].put(log)

    def analize_logs(self, log:Ssh_log) -> None:
        
        self.clean_time(log.date)
        self.add_log_to_dict(log)    
        
        for key,velue in self.potential_attacks.items():
            if velue.qsize() > 5:
                if key not in self.attacs.keys():
                    self.attacs[key] = []
                for queue_values in list(velue.queue):
                    if queue_values not in self.attacs[key]:
                        self.attacs[key].append(queue_values)
        
    def run_for_user(self) -> None:
        
        for log in self.logs:
            if get_message_type(log) == MessageType.InvalidPassword:
                if get_user_from_message(log) == self.user:
                    self.analize_logs(log)

    def run_for_all(self) -> None:
        for log in self.logs:
            if get_message_type(log) == MessageType.InvalidPassword:
                self.analize_logs(log)
            
        
    def clean_time(self, current_time:datetime) -> dict:
        
        for key in self.potential_attacks:
            while( self.potential_attacks[key].qsize() > 0):
                if(current_time - self.potential_attacks[key].queue[0].date).total_seconds() > self.duration:
                    self.potential_attacks[key].get()
                    # print(self.potential_attacks[key].qsize())
                else:
                    break
        return self.potential_attacks