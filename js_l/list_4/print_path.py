import os,sys

def print_path(path: str) -> None:
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            print(f"Path: {os.path.join(path, i)}")
            for j in os.listdir(os.path.join(path, i)):
                if not os.path.isdir(os.path.join(path, i, j)):
                    print(f'\t- {os.path.join(path, i, j)}')

print_path(os.environ["HOME"])