from lab_3_a import check_code

def read_data() -> None:   
    while True:
        try:
            line = input()
            if len(line) != 0:
                if check_code(line, "200"): print(line)

        except EOFError:
            break

if __name__ == "__main__":
    read_data() 