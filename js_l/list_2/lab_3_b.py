
def get_sent_bytes(data) -> str:
    return data.split(" ")[-1]

def return_send_bytes(data:str) -> int: 
    """return the number of bytes sent"""
    bytes = get_sent_bytes(data)
    
    try:
        bytes = int(bytes)
    except ValueError:
        bytes = 0
    return bytes    


def read_data(): 
    sent_data = 0  
    while True:
        try:
            line = input()
            if len(line) != 0:
                sent_data += return_send_bytes(line)
            
        except EOFError:
            break
        
    print(f"Sent bytes: {sent_data} B")
    print(f"Sent gigabytes: {sent_data/(1024**3)} GB")
    
if __name__ == "__main__":
    read_data()