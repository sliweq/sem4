from functions import *

# 199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245
# unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] "GET /shuttle/countdown/ HTTP/1.0" 200 3985

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
