import os,sys

def print_environ(env:os._Environ, args: list) -> None:
    if len(args) == 1:
        for k in sorted(env.items()):
            print(f'{k[0]} - {k[1]}')
    else:
        for k in sorted(env.items()):
            for i in args[1:]:
                if i.lower() not in k[1].lower():
                    break
                else:
                    print(f'{k[0]} - {k[1]}')
            # if False in tmp:
            #     continue
            # print(f'{k[0]} - {k[1]}')
                
                    
if __name__ == '__main__':
    print_environ(os.environ, sys.argv)
