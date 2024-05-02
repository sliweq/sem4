import typer
import os 
from ssh_utils import *
from main import read_logs
import logging
from setup_logging import setup_logging

logger = logging.getLogger()
app = typer.Typer()

@app.command()
def ex5(filename:str, duration:int, user_in:str = None):
    if not os.path.exists(filename):
        logger.warning(f"File {filename} does not exist")
        return
    
    if not user_in:
        try:    
            duration = int(duration)
        except ValueError:
            duration = 300
        logs = []
        for log in read_logs(filename):
            if get_message_type(log) == MessageType.InvalidPassword:
                logs.append(log)
        
        print(BruteForce(logs, duration).run())
    else:
        try:    
            duration = int(duration)
        except ValueError:
            duration = 300
        user = user_in
        
        logs = []
        for log in read_logs(filename):
            if get_message_type(log) == MessageType.InvalidPassword:
                logs.append(log)
        print(BruteForce(logs, duration, user).run())

@app.command()
def ex2(filename:str, excercise:int):
    if not os.path.exists(filename):
        logger.warning(f"File {filename} does not exist")
        return
    
    for log in read_logs(filename):
        if excercise == 1:
            print(log)
        elif excercise == 2:
            ipv4 = get_ipv4s_from_log(log)
            if ipv4:
                print(ipv4)
        elif excercise == 3:    
            users = get_user_from_message(log)
            if users:
                print(users)
        elif excercise == 4:
            print(get_message_type(log).name)


@app.command()
def ex4(filename:str, excercise:int):
    if not os.path.exists(filename):
        logger.warning(f"File {filename} does not exist")
        return
    
    logs = []
    for log in read_logs(filename):
        
        logs.append(log)
    if excercise == 1:
        get_n_logs(logs,10)
    elif excercise == 2:
        average_connection_time(logs)
    elif excercise == 3:
        get_most_less_active_user(logs) 
             
if __name__ == "__main__":
    app()
    
    