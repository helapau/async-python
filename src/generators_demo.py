"""
generator functions
"""
from typing import List, Generator


def fib(n: int) -> List[int]:
    """fibonacci numbers up to n using lists """
    numbers = [0, 1]
    i = 1
    if n <= i:
        return numbers
    else:
        while i < n:
            numbers.append(numbers[i] + numbers[i-1])
            i += 1
    return numbers
# fibonacci sequence is infinite but this function takes in a finite N to know when to stop creating the list


def fib_gen() -> Generator[int, None, None]:
    """generate fibonacci numbers"""
    f1 = 0
    yield f1
    f2 = 1
    yield f2
    i = 1
    while True:
        current = f1 + f2
        yield current
        f1 = f2
        f2 = current
        i += 1


if __name__ == "__main__":
    numbers_gen = fib_gen() # returns a generator object
    for f in numbers_gen:
        print(f, end=', ')
        if f > 10_000:
            break
    print("Done")




