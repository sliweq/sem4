
def get_failed_reads(logs:list, param:bool = True) -> list:
    """Excercise 2, subpoint e
        param: bool, default True - if True, return all logs, if False, return logs in two lists
    """
    new_logs_4 = []
    new_logs_5 = []
    for log in logs:
        if log[4] // 100 == 5:
            new_logs_5.append(log)
        elif log[4] // 100 == 4:
            new_logs_4.append(log)
    if param:
        return new_logs_4 + new_logs_5
    return [new_logs_4,new_logs_5]

if __name__ == "__main__":
    from read_log import read_log
    logs = read_log()
    print(get_failed_reads(logs, False)[1])