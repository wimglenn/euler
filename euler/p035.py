"""
The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""
from euler import primes, Primes

result = sum(1 for p in primes(1000000) if all(int(str(p)[n:] + str(p)[:n]) in Primes for n in range(1, len(str(p)))))
