
def get_failed_reads(logs:list) -> list:
    """Excercise 2, subpoint e"""
    new_logs = []
    for log in logs:
        if log[4] // 100 == 5 or log[4] // 100 == 4:
            new_logs.append(log)
    return new_logs

if __name__ == "__main__":
    from read_log import read_log
    logs = read_log()
    get_failed_reads(logs)