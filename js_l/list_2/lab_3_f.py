def get_date(data:str) -> str:
    """return the date from the raw data"""
    try:
        return data.split("[")[1].split("]")[0].split(" ")[0]
    except IndexError:
        return ""

def get_time(data:str) -> str:
    """return the time from the data"""
    for i in range(len(data)):
        if data[i] == ":":
            if i + 1 < len(data): 
                return data[i+1:]
    
    raise ValueError("No time in data")
        
def get_hour(data:str) -> str:
    """return the date from the raw data"""
    try:
        return data.split(":")[0]
    except IndexError:
        return ""

def read_data() -> None:   
    while True:
        try:
            line = input()
            if len(line) != 0:
                date = get_date(line)
                try:
                    time = get_time(line)
                except ValueError:
                    time = ""
                if time != "":
                    hour = get_hour(time)
                    try:
                        hour = int(hour)
                        if hour >= 22 or hour <= 6:
                            print(line)
                    except ValueError:
                        pass
                    
        except EOFError:
            break
    
if __name__ == "__main__":
    read_data()
