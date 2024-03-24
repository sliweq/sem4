from enum import Enum
from typing import Optional
from read_log import read_log

class ExtensionsType(Enum):
    GIF = 1
    JPG = 2
    JPEG = 3
    XBM = 4

def get_entires_by_extension(logs:list, extension:ExtensionsType = ExtensionsType.GIF) -> Optional[list]:
    """Excercise 2, subpoint f"""
    new_logs = []
    match extension:
        case ExtensionsType.GIF:
            for log in logs:
                if log[3].endswith(".gif"):
                    new_logs.append(log)
        case ExtensionsType.JPG:
            for log in logs:
                if log[3].endswith(".jpg"):
                    new_logs.append(log)
        case ExtensionsType.JPEG:
            for log in logs:
                if log[3].endswith(".jpeg"):
                    new_logs.append(log)
        case ExtensionsType.XBM:
            for log in logs:
                if log[3].endswith(".xbm"):
                    new_logs.append(log)
        case _: raise ValueError("Invalid extension")
    return new_logs


if __name__ == "__main__":
    get_entires_by_extension(read_log(), ExtensionsType.XBM)