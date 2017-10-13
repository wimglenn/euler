"""
A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91  99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""
from itertools import combinations

result = max(x * y for x, y in combinations(range(100, 1000), 2) if str(x * y) == str(x * y)[::-1])
