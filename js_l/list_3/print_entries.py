
def print_entries(logs:list) -> None:
    """Excercise 2, subpoint g"""
    for log in logs:
        print(log)

if __name__ == "__main__":
    from read_log import read_log
    logs = read_log()
    print_entries(logs)