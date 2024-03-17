
from lab_3_c import get_path_from_data

def read_data() -> None: 
    data_d = {".gif":0,".jpg":0,".jpeg":0,".xbm":0}
    
    while True:
        try:

            line = input()
            
            if len(line) != 0:
                path = get_path_from_data(line)
                if len(path) > 0:
                    if ".gif" in path: data_d[".gif"] += 1 # if .gif" == path[-4:]: data_d[".gif"] += 1
                    elif ".jpg" in path: data_d[".jpg"] += 1
                    elif ".jpeg" in path: data_d[".jpeg"] += 1
                    elif ".xbm" in path: data_d[".xbm"] += 1
            
        except EOFError:
            break
    all_files = sum(data_d.values())
    print(f"gif: {data_d['.gif']} ({data_d['.gif']/all_files*100}%)")
    print(f"jpg: {data_d['.jpg']} ({data_d['.jpg']/all_files*100}%)")
    print(f"jpeg: {data_d['.jpeg']} ({data_d['.jpeg']/all_files*100}%)")
    print(f"xbm: {data_d['.xbm']} ({data_d['.xbm']/all_files*100}%)")
    
if __name__ == "__main__":
    read_data()    
