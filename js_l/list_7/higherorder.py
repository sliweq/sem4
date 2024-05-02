

def forall(pred, iterable) -> bool:
    for item in iterable:
        if not pred(item):
            return False
    return True

def exists(pred, iterable) -> bool:
    for item in iterable:
        if pred(item):
            return True
    return False

def atleast(n, pred, iterable) -> bool:
    count = 0
    for item in iterable:
        if pred(item):
            count += 1
            if count >= n:
                return True
    return False

def atmost(n, pred, iterable) -> bool:
    count = 0
    for item in iterable:
        if pred(item):
            count += 1
            if count > n:
                return False
    return True