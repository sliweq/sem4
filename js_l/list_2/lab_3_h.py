def get_ip_and_domain(data:str) -> str:    
    return data.split(" ")[0]

def contains_pl_domain(data:str) -> bool:
    return data[-3:] == ".pl" 

def read_data() -> None:   
    while True:
        try:
            line = input()
            if len(line) != 0:
                try:
                    ip_domain = get_ip_and_domain(line)
                    if contains_pl_domain(ip_domain): print(line)
                except IndexError:
                    pass
                
        except EOFError:
            break
    
if __name__ == "__main__":
    read_data()