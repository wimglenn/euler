"""
The sum of the squares of the first ten natural numbers is,

1^2 + 2^2 + ... + 10^2 = 385
The square of the sum of the first ten natural numbers is,

(1 + 2 + ... + 10)^2 = 55^2 = 3025
Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025  385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.
"""
s = (100 * (100 + 1)) // 2
brute_force_s = sum(range(101))
assert s == brute_force_s
result = sum(x * (s - x) for x in range(101))
brute_force_result = sum(range(101)) ** 2 - sum(x ** 2 for x in range(101))
assert result == brute_force_result
result = result
