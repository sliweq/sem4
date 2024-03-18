import datetime
from lab_3_f import get_date


def get_str_date(data:str) -> str:
    """return the date from the raw data"""
    try:
        return data.split(":")[0]
    except IndexError:
        return ""

def get_datetime(data:str) -> datetime.datetime:
    return datetime.datetime.strptime(data, "%d/%b/%Y")

def read_data() -> None:   
    while True:
        try:
            line = input()
            if len(line) != 0:
                try:
                    date = get_date(line)
                    date = get_str_date(date)
                    date = get_datetime(date)
                    if date.isoweekday() == 5:
                        print(line)
                except ValueError:
                    pass
        except EOFError:
            break
    
if __name__ == "__main__":
    read_data()