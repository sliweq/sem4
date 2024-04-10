import subprocess,sys,os, logging, csv

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

def run():
    sum_read_files = 0
    sum_chars = 0
    sum_words = 0
    sum_lines = 0
    most_common_char = ""
    most_common_word = ""
    
    # print(get_path())
    
    x = subprocess.run(["./analise_file", "tmp.txt"],  encoding='ascii', capture_output=True)
    y = csv.reader(x.stdout.splitlines())
    for y in y:
        print(y)    

if __name__ == '__main__':
    run()