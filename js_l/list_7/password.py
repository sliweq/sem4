import random
import logging
import time

logging.basicConfig(level=logging.DEBUG)
def log(level):
    def decorator(func_or_class):
        logger = logging.getLogger(func_or_class.__module__)
        logger.setLevel(level)

        def wrapper(*args, **kwargs):
            timer = time.time()
            if isinstance(func_or_class, type): # class 
                logger.log(level, f"Initialization {func_or_class.__name__} with args: {args}, kwargs: {kwargs}")
                insatnce = func_or_class(*args, **kwargs)
                logger.log(level, f"Created object {func_or_class.__name__} in time {time.time() - timer}.")
                return insatnce
            else:  # func 
                func_name = func_or_class.__name__
                logger.log(level, f"Called {func_name} with args: {args}, kwargs: {kwargs}")
                result = func_or_class(*args, **kwargs)
                logger.log(level, f"Function {func_name} returned {result} in time {time.time() - timer}")
                return result

        return wrapper
    return decorator

@log(logging.DEBUG)
class PasswordGenerator:
    def __init__(self, length: int, charset : str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", count: int = 1) -> None:
        self.length = length
        self.charset = charset
        self.count = count
        

    def __iter__(self) :
        return self
    
    @log(logging.DEBUG)
    def __next__(self) -> str:
        if self.count == 0:
            raise StopIteration
        else:
            self.count -= 1
            return ''.join(random.choices(self.charset, k=self.length))
    
p = PasswordGenerator(10, count=5)
# print(next(p))
# print(next(p))
# print(next(p))
# print(next(p))
# print(next(p))
# print(next(p))

for passwd in p:
    print(passwd)