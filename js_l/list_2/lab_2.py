# 199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245
# unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] "GET /shuttle/countdown/ HTTP/1.0" 200 3985

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