
def read_log():
    while True:
            try:
                line = input()
            except EOFError:
                break