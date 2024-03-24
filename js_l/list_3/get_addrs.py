from read_log import read_log
from entry_to_dict import entry_to_dict
def get_addrs(logs:dict) -> list:
    """Excercise 3, subpoint c"""
    return list(logs.keys())

if __name__ == "__main__":
    print(get_addrs(entry_to_dict(read_log()[0])))