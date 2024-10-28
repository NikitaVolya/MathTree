
def fib(n: int) -> int:
    n = int(n)
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
    return a


def GCD(a: int, b: int):
    while b != 0:
        tmp = a % b
        a = b
        b = tmp
    return a


def PPCM(a: int, b: int):
    return abs(a * b) / GCD(a, b)

