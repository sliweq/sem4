from entry_to_dict import entry_to_dict
from read_log   import read_log

def log_to_dict(logs:list) -> dict:
    """Excercise 3, subpoint b"""
    logs_dict = {}
    for log in logs:
        try:
            logs_dict[log[0]].append(entry_to_dict(log))
        except KeyError:
            logs_dict[log[0]] = []
            logs_dict[log[0]].append(entry_to_dict(log))
    return logs_dict

if __name__ == "__main__":
    logs_dict = log_to_dict(read_log())
    print(list(logs_dict.values())[0])