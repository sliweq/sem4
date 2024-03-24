
def get_entries_by_addr(logs:list, addr:str = "199.72.81.55") -> list:
    """Excercise 2, subpoint c"""
    new_logs = []
    for log in logs:
        if log[0] == addr:
            new_logs.append(log)
    return new_logs

if __name__ == "__main__":
    from read_log import read_log
    logs = read_log()
    try:
        print(get_entries_by_addr(logs, "199.72.81.55")[:4])
    except IndexError:
        print(get_entries_by_addr(logs, "199.72.81.55"))