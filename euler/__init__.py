#!/usr/bin/env python3
"""
http://projecteuler.net/
"""
import json
import math
import sys
import itertools as it
import operator as op
from argparse import ArgumentParser
from functools import reduce
from importlib import import_module
from pathlib import Path
from timeit import Timer


def my_timeit(func, *args, **kwargs):
    """Uses timeit to wrap a function and return execution time along with the result"""
    output_container = []

    def wrapper():
        output_container.append(func(*args, **kwargs))

    timer = Timer(wrapper)
    delta = timer.timeit(1)
    return delta, output_container.pop()


def squares():
    """generator yielding 1, 4, 9, 16..."""
    return (n * n for n in it.count(1))


def isqrt(n):
    """integer square root.  uses newton's method"""
    if n == 0:
        return 0
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    if x ** 2 != n:
        raise ValueError('input was not a perfect square')
    return x


def multiplicative_order(a, n):
    """In number theory, given an integer a and a positive integer n with gcd(a,n) = 1, the multiplicative order of a modulo n is the smallest positive integer k with a**k congruent to 1 (mod n)"""
    if gcd(a, n) != 1:
        raise ValueError('Input numbers should be co-prime')
    for k in it.count(1):
        if (a ** k) % n == 1:
            return k


def collatz(n, memo={1: [1]}):
    """The following iterative sequence is defined for the set of positive integers:

    n -> n/2 (n is even)
    n -> 3n + 1 (n is odd)

    Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

    >>> collatz(1)
    [1]
    >>> collatz(13)
    [13, 40, 20, 10, 5, 16, 8, 4, 2, 1]"""
    if n not in memo:
        memo[n] = [n] + collatz(3 * n + 1 if n % 2 else n // 2)
    return memo[n]


def collatz_length(n, memo={1: 1}):
    if n not in memo:
        memo[n] = 1 + collatz_length(3 * n + 1 if n % 2 else n // 2)
    return memo[n]


def triangle(n):
    """triangle numbers

    triangle(n) = sum(1, 2, 3 ... n)"""
    return n * (n + 1) // 2


def triangles():
    """generator yielding 1, 3, 6, 10, 15..."""
    return (triangle(n) for n in it.count(1))


def pentagonal(n):
    """returns the nth pentagonal number"""
    return n * (3 * n - 1) // 2


def pentagonals():
    """generator yielding consecutive pentagonal numbers"""
    return (pentagonal(n) for n in it.count(1))


def fib_r(n, memo={0: 0, 1: 1}):
    """recursive fibonacci numbers generation with memoisation

    >>> [fib_r(n) for n in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    >>> print(fib_r(100))
    354224848179261915075"""
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]


def fib_gen():
    """fibonacci number generator
    """
    yield 0
    f_, f = 0, 1
    while True:
        yield f
        f_, f = f, f + f_


def fib_i(n):
    """iterative fibonacci numbers

    >>> [fib_i(n) for n in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    >>> print(fib_i(100))
    354224848179261915075"""
    return next(it.islice(fib_gen(), n, n + 1))


fib = fib_r


def is_prime(n, memo={1: False, 2: True, 3: True}):
    """brute force primality test

    >>> is_prime(99)
    False
    >>> is_prime(104729)
    True
    >>> [x for x in range(20) if is_prime(x)]
    [2, 3, 5, 7, 11, 13, 17, 19]"""
    if n not in memo:
        memo[n] = False if n % 2 == 0 or n <= 0 else all(n % i for i in range(3, int(1 + math.sqrt(n)), 2))
    return memo[n]


def primes(n):
    """prime sieve, lists primes less than n

    >>> primes(2)
    []
    >>> primes(7)
    [2, 3, 5]
    >>> primes(8)
    [2, 3, 5, 7]
    >>> sum(primes(111))
    1480"""
    if n <= 2:
        return []
    r = [True] * n
    r[0] = r[1] = False
    r[4::2] = [False] * len(r[4::2])
    for i in range(int(1 + math.sqrt(n))):
        if r[i]:
            r[3*i::2*i] = [False] * len(r[3*i::2*i])
    return [i for i, x in enumerate(r) if x]


class SetOfThings:

    """A set-like abstraction which hides a callable deterministic test"""

    def __init__(self, test_callable):
        self.test_callable = test_callable
        self.memo = {}

    def __contains__(self, n):
        if n not in self.memo:
            self.memo[n] = self.test_callable(n)
        return self.memo[n]


Primes = SetOfThings(is_prime)


def is_pentagonal(n):
    try:
        x = isqrt(24 * n + 1)
    except ValueError:
        return False
    return (x + 1) % 6 == 0


def is_hexagonal(n):
    try:
        x = isqrt(8 * n + 1)
    except ValueError:
        return False
    return (x + 1) % 4 == 0


Pentagonals = SetOfThings(is_pentagonal)
Hexagonals = SetOfThings(is_hexagonal)


def factorise(n):
    """returns the sorted prime factors of natural number n

    >>> factorise(12)
    [2, 2, 3]
    >>> factorise(4998)
    [2, 3, 7, 7, 17]
    >>> factorise(4999)
    [4999]"""
    if n < 0:
        result = factorise(-n)
        result[0] *= -1
        return result
    for i in range(2, int(1 + math.sqrt(n))):
        if n % i == 0:
            return [i] + factorise(n // i)
    else:
        return [n]


def gcd(a, b):
    """greatest common divisor"""
    return gcd(b, a % b) if b else a


def lcm(a, b):
    """least common multiple"""
    return abs(a * b) // gcd(a, b)


def divisors(n):
    """sorted list of divisors of natural number n

    >>> divisors(100)
    [1, 2, 4, 5, 10, 20, 25, 50, 100]
    >>> divisors(9973)
    [1, 9973]"""
    factors = factorise(n)
    return sorted(set(reduce(op.mul, c, 1) for i in range(len(factors) + 1) for c in it.combinations(factors, i)))


def palindrome(s):
    return str(s).lower() == str(s).lower()[::-1]


def unique_digits(n):
    """helper function for checking pandigitals

    >>> unique_digits(12345)
    True
    >>> unique_digits('12345')
    True
    >>> unique_digits(1233)
    False"""
    return len(str(n)) == len(set(str(n)))


def nCr(n, r, memo={}):
    if (n, r) not in memo:
        memo[n, r] = memo[n, n-r] = math.factorial(n) // (math.factorial(r) * math.factorial(n-r))
    return memo[n, r]


def get_result(modname):
    module = import_module(f'euler.{modname}')
    return getattr(module, 'result', None)


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    parser = ArgumentParser("Wim's project euler progress")
    parser.add_argument('--all', action='store_true')
    parser.add_argument('ids', type=int, nargs='*', default=[])
    args = parser.parse_args()

    here = Path(__file__).parent
    sys.path.append(str(here.parent))
    my_answers = json.loads((here/'../data/my_answers.json').read_text())
    if args.ids:
        problems = [f'p{n:03d}' for n in args.ids]
    else:
        problems = [p.name[:-3] for p in here.glob('p*.py')]
        if not args.all:
            problems = [max(problems)]

    total_time = 0
    for p in sorted(problems):
        delta, answer = my_timeit(get_result, p)
        total_time += delta
        if answer is not None and type(answer) is not int:
            print(f'{p} result is instance {type(answer)}, expected int')
        print(f' {p}: {answer:16d} ({delta:.02f}s)')
        assert answer == my_answers[p]

    if len(problems) > 1:
        print('-' * 40)
        print(f' total time : {total_time:.02f} s')
