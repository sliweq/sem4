from typing import Generator
from setup_logging import setup_logging
import logging
import os
from ssh_utils import * 
from ssh_class import Ssh_log
import argparse


parser = argparse.ArgumentParser(prog='list_5')
parser.add_argument("filename", help="File with logs")
parser.add_argument("-l", "--log", type=str, help="Type of logging")
subparsers = parser.add_subparsers(dest="subcommand",required=True)
parser_ex2 = subparsers.add_parser("ex2")
parser_ex2.add_argument("arg2", type=int, help="Number of subpoint excerise 2")
parser_ex4 = subparsers.add_parser("ex4")
parser_ex4.add_argument("arg4", type=int, help="Number of subpoint excerise 4")


args = parser.parse_args()

logger = logging.getLogger()

LOG_LEVEL = args.log
setup_logging(LOG_LEVEL)



def read_logs(name:str) -> Generator[Ssh_log, None, None]:
    # zadanie 2 a 
    # Generator[yield_type, send_type, return_type] 
    with open(name,"r") as file:
        for line in file:
            line = line.strip().split()
            date = get_date_from_log(line[0],line[1],line[2])
            message = get_message_from_log(line)
            
            if line and date and message:
                yield Ssh_log(date, line[3], get_sshd_from_log(line[4]), message)

            else:
                logger.warning(f"Line {line} is not valid")
                

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

if __name__ == "__main__":
    run()
    
