import random
from typing import Generator


class PasswordGenerator:
    def __init__(self, length: int, charset : str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", count: int = 1) -> None:
        self.length = length
        self.charset = charset
        self.count = count
        

    def __iter__(self) :
        return self

    def __next__(self) -> str:
        if self.count == 0:
            raise StopIteration
        else:
            self.count -= 1
            return ''.join(random.choices(self.charset, k=self.length))
    
# p = PasswordGenerator(10, count=5)
# print(next(p))
# print(next(p))
# print(next(p))
# print(next(p))
# print(next(p))
# print(next(p))

# for passwd in p:
#     print(passwd)