
def read_data(): # excerise 2    
    while True:
        try:
            line = input()
            if find_eof(line):
                print("EOF")
                break
            print(line)
            
        except EOFError:
            break

def find_eof(data) -> bool:
    return "eof" in data.lower()

read_data()