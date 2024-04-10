from read_log import read_log
from log_to_dict import log_to_dict


def print_dict_entry_dates(logs:dict) -> None:
    """Excercise 3, subpoint d"""
    for addr, entries in logs.items():
        print(f"Addres: {addr}", end=" ")
        print(f"| Entries: {len(entries)}", end=" ")
        print(f"| Dates:Q{entries[0]['date']}/{entries[0]['time']}-{entries[-1]['date']}/{entries[-1]['time']}", end=" ")
        print(f"| Codes ratio: {round((len(list(filter(lambda x: x['code'] == 200 ,entries)))/len(entries))*100,2)}%")

if __name__ == "__main__":
    print_dict_entry_dates(log_to_dict(read_log()))