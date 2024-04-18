import subprocess,sys,os, logging, csv
from typing import Optional


def find_most_freq(list_of_words: list[str]) -> str:
    counter = 0
    num = list_of_words[0]
     
    for i in list_of_words:
        curr_frequency = list_of_words.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num

def get_path() -> Optional[str]:
    return sys.argv[1] if len(sys.argv) > 1 else None

def read_files( path:str ) -> None:
    sum_read_files = 0
    sum_chars = 0
    sum_words = 0
    sum_lines = 0
    most_common_char = []
    most_common_word = []
     
    for file in os.listdir(path):
        if file.endswith(".txt"):

            output = subprocess.run(["./analise_file", os.path.join(path, file)],  encoding='ascii', capture_output=True)
            csv_output = csv.reader(output.stdout.splitlines())
            for row in csv_output:
                match row[0]:
                    case "1":
                        sum_read_files += 1
                    case "2":
                        sum_chars += int(row[1])
                    case "3":
                        sum_words += int(row[1])
                    case "4":
                        sum_lines += int(row[1])
                    case "5":
                        most_common_char.append(row[1])
                    case "6":
                        most_common_word.append(row[1])
    print (f"Number of files read: {sum_read_files}")
    print (f"Number of characters: {sum_chars}")
    print (f"Number of words: {sum_words}")
    print (f"Number of lines: {sum_lines}")
    print (f"Most common character: '{find_most_freq(most_common_char)}'")
    print (f"Most common word: {find_most_freq(most_common_word)}")

def run():
    path = get_path()
    if path:    
        if os.path.exists(path):
            read_files(path)
        else:
            logging.error(f"Path {path} does not exist")
    else:
        logging.error("No path provided")
         

if __name__ == '__main__':
    run()