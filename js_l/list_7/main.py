from functools import reduce


def acronym(phrases:list[str]) -> str:
    phrases = list(map(lambda x: x[0], phrases))
    return ''.join(phrases)

def median(numbers: list[float]) -> float:
    numbers.sort()
    return numbers[len(numbers)/2] if len(numbers) % 2 == 1 else (numbers[len(numbers)/2] + numbers[len(numbers)/2 - 1]) / 2


def pierwiastek(x : float, epsilon:float) -> float:
    def pierwiastek_iter(y:float) -> float:
        return (abs(y * y - x) > epsilon and pierwiastek_iter((y + x / y)/2)) or y
    return pierwiastek_iter(x/2)
    
def make_alpha_dict(alpha: str) -> dict[str, list[str]]:
    alpha_dict = dict(map(lambda x: (x,list(filter(lambda y: x in y,alpha.split()))), "".join(alpha.split())))
    return alpha_dict
    
def flatten(unknown_list : list) -> list:
    return reduce(lambda x, y: x + y, map(flatten, filter(lambda x: isinstance(x, list), unknown_list)),list(filter(lambda x: not isinstance(x, list), unknown_list)))

print(flatten([1,[2,3],1]))    