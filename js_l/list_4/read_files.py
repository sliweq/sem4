import subprocess,sys,os, logging

logger = logging.getLogger(__name__)

def get_path() -> str:
    return sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

def read_files( path:str ) -> None:
    pass

def run():
    path = get_path()
    if os.path.exists(path):
        read_files(path)
    else:
        logger.error(f"Path {path} does not exist")

if __name__ == '__main__':
    # print(get_path())
    
    subprocess.run(["./analise_file", "tmp.txt"])
    while True:
        try:
            line = input()
            print(f"python line: {line}")
            
        except EOFError:
            break