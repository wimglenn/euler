"""
A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:

1/2  = 0.5
1/3  = 0.(3)
1/4  = 0.25
1/5  = 0.2
1/6  = 0.1(6)
1/7  = 0.(142857)
1/8  = 0.125
1/9  = 0.(1)
1/10 = 0.1
Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
"""
# from Fermat's little theorem, the period of the repeating decimal of 1 / p
# is equal to the order of 10 modulo p.  If 10 is a primitive root modulo p,
# the period is equal to p - 1; if not, the period is a factor of p - 1.
from euler import multiplicative_order, primes

result = max(primes(1000)[4:], key=lambda x: multiplicative_order(10, x))
