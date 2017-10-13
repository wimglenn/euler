"""
An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the following expression.

d1 * d10 * d100 * d1000 * d10000 * d100000 * d1000000
"""
from functools import reduce
from itertools import count
from operator import mul

s = '.'
for i in count(1):
    s += str(i)
    if len(s) > 1000000:
        result = reduce(mul, [int(s[10 ** d]) for d in range(7)], 1)
        break
