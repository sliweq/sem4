import os, sys, time
from typing import Optional
from queue import Queue

ARGUMENTS = ["--lines", "--follow"]

def check_args(args:str) -> bool:
    for arg in ARGUMENTS:
        if len(args) < len(arg):
            continue
        if arg == args[:len(arg)]:
            return True
        
    return False

def get_lines(arg:str) -> Optional[int]:
    if arg[:7] != ARGUMENTS[0]:
        return None
    try:
        number = int(arg[8:])
    except ValueError:
        return None 
    if number < 0:
        return None
    return number

def get_follow(args:list) -> bool:
    for arg in args:
        if arg == ARGUMENTS[1]:
            return True
    return False

def run() -> None:
    file_name = None
    for i in sys.argv[1:]:
        
        if i[0] == "-" or i[:1] == "--":
            if not check_args(i):
                raise SyntaxError(f"Invalid argument: {i} \t Valid arguments: {ARGUMENTS}")
            
        elif not os.path.exists(os.path.join(os.getcwd(), i)):
            raise FileNotFoundError(f"File {i} not found")
        else:
            file_name = os.path.join(os.getcwd(), i)
            
    
    lines_to_read = 10
    for i in sys.argv[1:]:
        if get_lines(i):
            lines_to_read = get_lines(i)
            
    if lines_to_read == 0:
        return
    if file_name:
        read_from_file(file_name, lines_to_read, get_follow(sys.argv[1:]))
    else:
        read_from_input(lines_to_read)
    
def read_from_file(file:str, lines:int, follow:bool = False) -> None:
    with open(file, "r") as f:
        if follow:
            f.seek(0) 
            q = Queue()
            file_size = os.stat(file).st_size
            while 1:
                f.tell()
                line = f.readline()
                
                if not line:
                    if q.qsize() == lines:
                        break
                        
                    time.sleep(1)
                    
                    current_size = os.stat(file).st_size
                    if current_size != file_size:
                        q.queue.clear()
                        f.seek(0)
                        
                else:
                    q.put(line)
                    if q.qsize() > lines:
                        q.get()
            
            while not q.empty():
                print(q.get(), end="")
            
        else:
            q = Queue()
            for line in f:
                q.put(line)
                if q.qsize() > lines:
                    q.get()
            while not q.empty():
                print(q.get(), end="")        

def read_from_input(lines:int) -> None:
    q = Queue()
    while True:
            try:
                line = input()
                q.put(line)
                if q.qsize() > lines:
                    q.get()
                    
            except EOFError:
                break
    while not q.empty():
        print(q.get(), end="")


if __name__ == '__main__':   
    run()    