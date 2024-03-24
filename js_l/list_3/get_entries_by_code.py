
def get_entries_by_code(logs:list, code:int = 200) -> list:
    """Excercise 2, subpoint d"""
    new_logs = []
    for log in logs:
        if log[4] == code:
            new_logs.append(log)
    return new_logs

if __name__ == "__main__":
    from read_log import read_log
    logs = read_log()
    print(get_entries_by_code(logs, 404)[:4])
