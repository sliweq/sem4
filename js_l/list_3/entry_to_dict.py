from typing import Optional
from read_log import read_log

def entry_to_dict(log:tuple) -> Optional[dict]:
    """Excercise 3, subpoint a"""
    try:
        return {
            "addr": log[0],
            "date": log[1],
            "time": log[2],
            "path": log[3],
            "code": log[4],
            "size": log[5]
        }
    except IndexError:
        return None

if __name__ == "__main__":
    print(entry_to_dict(read_log()[0]))