import shutil
import subprocess,sys,os, logging, csv
from typing import Optional, Tuple
from datetime import datetime
import pandas as pd
import os

# logging.basicConfig(
#      format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#      datefmt='%H:%M:%S'
#  )

def read_csv_file(path:dir) -> pd.DataFrame:
    if not os.path.exists(f"{path}/backups.csv"):
        sys.exit(f"File {path}/backups.csv does not exist")
    df = pd.read_csv(f'{path}/backups.csv',index_col=False, header=None)
    return df

def print_csv_file(df:pd.DataFrame) -> Tuple[str, str] :
    print("History of backups:")
    for index, row in df.iterrows():
        date_format = "%Y.%m.%d-%H:%M:%S"
        date = datetime_object = datetime.strptime(row[0], date_format)
        path = row[1]
        name = row[2].split("/")[-1]
        print(index, "-Date: ", date, "Path: ", path, "File name: ", name)
    
    chosen_file = input("Choose file to restore: ")
    while not chosen_file.isdigit() or int(chosen_file) < 0 or int(chosen_file) >= len(df):
        print("Srlsy? Invalid input")
        chosen_file = input("Choose file to restore: ")
    return (df.iloc[int(chosen_file)][1], df.iloc[int(chosen_file)][2])  
    
def move_and_restore(src_path:str,dst_path:str, file:str) -> None:
    if not os.path.exists(os.path.join(src_path, file)):
        sys.exit(f"File not found in {src_path}")
    
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    
    shutil.unpack_archive(os.path.join(dst_path, file), dst_path)
    remove_backups(src_path)
    
def remove_backups(path:str) -> None:
    print(path)
    if os.path.exists(f"{path}/backups.csv"):
        os.remove(f"{path}/backups.csv")

    for file in os.listdir(path):
        if file.endswith(".zip"):
            os.remove(os.path.join(path, file))


def get_path() -> Optional[str]:
    return sys.argv[1] if len(sys.argv) > 1 else None


def restore() -> None:
    path = get_path()      
      
    if not path:
        path = os.path.join(os.getcwd(), ".backup")
    if not os.path.exists(path):
        sys.exit(f"Path {path} does not exist")
    read_csv_file(path)
    path_file = print_csv_file(read_csv_file(path))
    move_and_restore(path, path_file[0], path_file[1])

if __name__ == "__main__":
    restore()