# 199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245
# unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] "GET /shuttle/countdown/ HTTP/1.0" 200 3985

from lab_3_b import return_send_bytes, get_sent_bytes

def get_path_from_data(data) -> str:
    return data.split(" ")[6]

def read_data(): 
    data_c = ("",0)
    while True:
        try:

            line = input()
            
            if len(line) != 0:
                if return_send_bytes(line) > data_c[1]:
                    path = get_path_from_data(line)
                    if len(path) > 0: data_c = (get_path_from_data(line), return_send_bytes(line))
            
        except EOFError:
            break
        
    print(f"Biggest file: {data_c[0]} with {data_c[1]} B")

if __name__ == "__main__":
    read_data()