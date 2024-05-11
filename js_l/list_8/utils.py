from typing import Optional
import datetime

def open_file(file_name:str) -> list[str]:
    lines = []
    with open(file_name, "r") as f:
        lines = f.readlines()
    return lines

def get_ip_or_domain(data: str) -> Optional[str]:
    try:
        return data.split()[0]
    except IndexError: 
        return None

def get_code(data:str) -> Optional[int]:
    try:
        return int(data.split()[-2])
    except IndexError or ValueError: 
        return None

def return_send_bytes(data:str) -> Optional[int]: 
    try:
        bytes = data.split(" ")[-1]
        if bytes == "-":
            return 0
        bytes = int(data.split(" ")[-1])
        return bytes
    except ValueError or IndexError:
        return None   

def get_path_from_data(data) -> Optional[str]:
    try:
        return data.split(" ")[6]
    except IndexError:
        return None

def get_method(data:str) -> Optional[str]:
    try:
        return data.split()[5][1:]
    except IndexError:
        return None

def get_time_zone(data:str) -> Optional[str]:
    try:
        zone = data.split()[4][:-1]
        return "UTC"+ zone[:3] + ":" + zone[3:]
    except IndexError:
        return None

def get_raw_date(data:str) -> Optional[str]:
    try:
        return data.split()[3][1:]
    except IndexError:
        return None


def get_full_date(date: str) -> Optional[datetime.datetime]:
    try:
        return datetime.datetime.strptime(date, "%d/%b/%Y:%H:%M:%S")
    except Exception:
        return None
 
def get_time(data: datetime.datetime) -> Optional[datetime.datetime]:
    return data.time()

def get_date(data: datetime.datetime) -> Optional[datetime.datetime]:
    return data.date()
    

def contains_pl_domain(data:str) -> Optional[bool]:
    try:
        return data[-3:] == ".pl" 
    except IndexError:
        return None