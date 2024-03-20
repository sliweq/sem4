from typing import Optional
import datetime

def get_ip_or_domain(data: str) -> Optional[str]:
    try:
        return data.split()[0]
    except IndexError: 
        return None

def get_code(data:str) -> Optional[str]:
    try:
        return data.split()[-2]
    except IndexError: 
        return None

def return_send_bytes(data:str) -> Optional[int]: 
    try:
        bytes = data.split(" ")[-1]
    except IndexError: 
        return None
    
    try:
        bytes = int(bytes)
        return bytes
    except ValueError:
        return None   


def get_path_from_data(data) -> Optional[str]:
    try:
        data.split(" ")[6]
    except IndexError:
        return None

def get_raw_date(data:str) -> Optional[str]:
    try:
        return data.split()[3][1:]
    except IndexError:
        return None


def get_date(date:str) -> Optional[datetime.datetime]:
    try:
        return datetime.datetime.strptime(date,"%d/%m/%y:%H:%M:%S")
    except Exception:
        return None
 

def contains_pl_domain(data:str) -> Optional[bool]:
    return data[-3:] == ".pl" 