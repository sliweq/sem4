from functions import *
def read_log() -> list:
    """Excercise 2, subpoint a"""
    all_logs = []
    while True:
            try:
                line = input()
                date = get_full_date(get_raw_date(line))
                single_log = (get_ip_or_domain(line), 
                                get_date(date),
                                get_time(date), 
                                get_path_from_data(line), 
                                get_code(line), 
                                return_send_bytes(line), 
                                )
                if not None in single_log:
                    all_logs.append(single_log)
            except EOFError:
                break
    return all_logs
