from typing import Generator
from setup_logging import setup_logging
import logging
import os
from ssh_utils import * 
from ssh_class import Ssh_log
import argparse

pattern = r'^(?P<date>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(?P<server>\S+)\s+sshd\[(?P<code>\d+)\]:\s+(?P<message>.*)$'

parser = argparse.ArgumentParser(prog='list_5')
parser.add_argument("filename", help="File with logs")
parser.add_argument("-l", "--log", type=str, help="Type of logging")
subparsers = parser.add_subparsers(dest="subcommand",required=True)
parser_ex2 = subparsers.add_parser("ex2")
parser_ex2.add_argument("arg2", type=int, help="Number of subpoint excerise 2")
parser_ex4 = subparsers.add_parser("ex4")
parser_ex4.add_argument("arg4", type=int, help="Number of subpoint excerise 4")
parser_ex5 = subparsers.add_parser("ex5")
parser_ex5.add_argument("ex5", nargs="*", metavar=("Duraton", "name"), help="Run brute force detector")

args = parser.parse_args()

logger = logging.getLogger()

LOG_LEVEL = args.log
setup_logging(LOG_LEVEL)



def read_logs(name:str) -> Generator[Ssh_log, None, None]:
    # zadanie 2 a 
    with open(name,"r") as file:
        for line in file:
            match = re.match(pattern,line)
            if match:
                date = get_date_from_log(match.group("date"))
                server = match.group('server')
                message = match.group('message')
                code = match.group('code')
                
                ssh_log = Ssh_log(date, server, code, message)
                #logger.debug(f"Read {len(line)} bytes")
                #report_log(ssh_log)
                yield ssh_log
                

def run() -> None:
    
    if not os.path.exists(args.filename):
        logger.warning(f"File {args.filename} does not exist")
        return None
    
    if args.subcommand == "ex2":
        for log in read_logs(args.filename):
            if args.arg2 == 1:
                print(log)
            elif args.arg2 == 2:
                ipv4 = get_ipv4s_from_log(log)
                if ipv4:
                    print(ipv4)
            elif args.arg2 == 3:    
                users = get_user_from_message(log)
                if users:
                    print(users)
            elif args.arg2 == 4:
                print(get_message_type(log).name)
    elif args.subcommand == "ex4":
        logs = []
        for log in read_logs(args.filename):
            
            logs.append(log)
        if args.arg4 == 1:
            get_n_logs(logs,10)
        elif args.arg4 == 2:
            average_connection_time(logs)
        elif args.arg4 == 3:
            get_most_less_active_user(logs)
    
    elif args.ex5:
        if len(args.ex5) == 1:
            try:    
                duration = int(args.ex5[0])
            except ValueError:
                duration = 300
            logs = []
            for log in read_logs(args.filename):
                if get_message_type(log) == MessageType.InvalidPassword:
                    logs.append(log)
            
            print(BruteForce(logs, duration).run())
        elif len(args.ex5) == 2:
            try:    
                duration = int(args.ex5[0])
            except ValueError:
                duration = 300
            user = args.ex5[1]
            
            logs = []
            for log in read_logs(args.filename):
                if get_message_type(log) == MessageType.InvalidPassword:
                    logs.append(log)
            print(BruteForce(logs, duration, user).run())
            

if __name__ == "__main__":
    run()
    
