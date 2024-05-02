from functools import cache
from time import time

def make_generator(f):
    x = 0
    while True:
        x += 1
        yield f(x)

def Fibonacci(n, a = 0, b = 1):
    if n == 1:
        return a
    else:
        return Fibonacci(n - 1, b, a + b)
    
def Fibonacci2(n):
    if n <= 1:
        return 0
    elif n == 2:
        return 1
    else:
        return Fibonacci(n - 1) + Fibonacci(n - 2)

@cache
def make_generator_mem(f):
    x = 0
    while True:
        x += 1
        yield f(x)
        
# timer = time()
# x = make_generator(Fibonacci2)
# for i in range(1000000):
#     pass
# print(next(x))
# print(time() - timer)
    
# timer = time()
# x = make_generator_mem(Fibonacci2)
# for i in range(1000000):
#     pass
# print(next(x))
# print(time() - timer)