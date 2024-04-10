from enum import Enum
from typing import Optional


class SortKey(Enum):
    IP = 1
    DATE = 2 
    TIME = 3
    PATH = 4
    CODE = 5
    BYTES = 6

def sort_log(log: list, key:SortKey = SortKey.IP) -> Optional[list]:
    """Excercise 2, subpoint b"""
    match key:
        case SortKey.IP: return sorted(log, key=lambda x: x[0])
        case SortKey.DATE: return sorted(log, key=lambda x: x[1])
        case SortKey.TIME: return sorted(log, key=lambda x: x[2])
        case SortKey.PATH: return sorted(log, key=lambda x: x[3])
        case SortKey.CODE: return sorted(log, key=lambda x: x[4])
        case SortKey.BYTES: return sorted(log, key=lambda x: x[5])
        case _: raise ValueError("Invalid key")

if __name__ == "__main__":
    from read_log import read_log
    logs = read_log()
    print(sort_log(logs, SortKey.IP))