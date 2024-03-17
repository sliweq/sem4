

def get_code(data:str) -> str:
    return data.split(" ")[-2]

def check_code(data:str, code:str) -> bool:
    return code == get_code(data)


def read_data() -> None:   
    
    code_200_amount = 0
    code_302_amount = 0
    code_404_amount = 0
    
    while True:
        try:
            line = input()
            if len(line) != 0:
                if check_code(line, "200"): code_200_amount += 1
                elif check_code(line, "302"): code_302_amount += 1
                elif check_code(line, "404"): code_404_amount += 1
        except EOFError:
            break
        
    print(f"200: {code_200_amount}\n302: {code_302_amount}\n404: {code_404_amount}")


if __name__ == "__main__":
    read_data()