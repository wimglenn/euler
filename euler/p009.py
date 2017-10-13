"""
A Pythagorean triplet is a set of three natural numbers, a  b  c, for which,

a^2 + b^2 = c^2
For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""
from itertools import combinations_with_replacement

for a, b in combinations_with_replacement(range(1, 501), 2):
    c = 1000 - a - b
    if a ** 2 + b ** 2 == c ** 2:
        break

result = a * b * c
