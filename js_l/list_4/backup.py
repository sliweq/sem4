import shutil
import subprocess,sys,os, logging, csv
from typing import Optional
from datetime import datetime
# logging.basicConfig(
#      format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#      datefmt='%H:%M:%S'
#  )

def write_csv_file(path:dir, backup_orign_path:str, backup_name:str) -> None:
    with open(f"{path}/backups.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y.%m.%d-%H:%M:%S"), backup_orign_path, backup_name])

        

def get_backup_dir() -> str:
    if os.environ.get("BACKUPS_DIR"):
        return os.environ.get("BACKUPS_DIR")
    else:
        return os.path.join(os.getenv("HOME"), ".backup")

def get_path() -> Optional[str]:
    return sys.argv[1] if len(sys.argv) > 1 else None

def move_backup(name:str) -> str:
    if not os.path.exists(get_backup_dir()):
        os.makedirs(get_backup_dir())
    if not os.path.exists(f"{get_backup_dir()}/{name}"):
        shutil.move(name, get_backup_dir())
        return f"{get_backup_dir()}/{name}"
    else:
        tmp = 0
        while os.path.exists(f"{get_backup_dir()}/{name} ({tmp})"):
            tmp+=1
        shutil.move(name, f"{get_backup_dir()}/{name} ({tmp})")
        return f"{get_backup_dir()}/{name} ({tmp})"

def create_backup() -> None:
    path = get_path()
    if path:
        if os.path.exists(get_path()):
            date_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            print(date_now)
            dir_name = os.path.basename(path)
            shutil.make_archive(f"{date_now}-{dir_name}", format="zip", root_dir=path)
            new_name = move_backup(f"{date_now}-{dir_name}.zip")
            print("xddd4")
            write_csv_file(get_backup_dir(), path, f"{new_name}")
        else:
            logging.error(f"Path {path} does not exist")
            return
    else:
        logging.error(f"Path does not provided")
        return

if __name__ == "__main__":
    create_backup()