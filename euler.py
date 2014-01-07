#!/usr/bin/env python3

"""
http://projecteuler.net/
"""
# pylint: disable=line-too-long,superfluous-parens,invalid-name

import os
import ast
import math
import time
import string
import collections
import itertools as it
import operator as op
import numpy as np
import datetime as dt
import argparse as ap
from functools import reduce

#--- util ---------------------------------------------------------------------


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
    r = [True for x in range(n)]
    r[0] = r[1] = False
    r[4::2] = [False] * len(r[4::2])
    for i, x in enumerate(r[:int(1 + math.sqrt(n))]):
        if x:
            r[3 * i::2 * i] = [False] * len(r[3 * i::2 * i])
    return [i for i, x in enumerate(r) if x]


class SetOfThings(object):

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
    if n == 1 or n == 2:
        return [n]
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
    return s.lower() == s.lower()[::-1]


def unique_digits(n):
    """helper function for checking pandigitals

    >>> unique_digits(12345)
    True
    >>> unique_digits('12345')
    True
    >>> unique_digits(1233)
    False"""
    return len(str(n)) == len(set(str(n)))


#------------------------------------------------------------------------------


def p001():
    """If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

    Find the sum of all the multiples of 3 or 5 below 1000."""
    return sum(x for x in range(1000) if x % 3 == 0 or x % 5 == 0)


def p002():
    """Each new term in the Fibonacci sequence is generated by adding the previous two terms. By starting with 1 and 2, the first 10 terms will be:

    1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

    By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms."""

    def fib_gen2():
        i = 0
        while fib(i) < 4 * 10 ** 6:
            if fib(i) % 2 == 0:
                yield fib(i)
            i += 1

    return sum(fib_gen2())


def p003():
    """The prime factors of 13195 are 5, 7, 13 and 29.

    What is the largest prime factor of the number 600851475143 ?"""
    return factorise(600851475143)[-1]


def p004():
    """A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91  99.

    Find the largest palindrome made from the product of two 3-digit numbers."""
    return max(x * y for x, y in it.combinations(range(100, 1000), 2) if str(x * y) == str(x * y)[::-1])


def p005():
    """2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

    What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?"""
    return reduce(lcm, range(20, 2, -1))


def p006():
    """The sum of the squares of the first ten natural numbers is,

    1^2 + 2^2 + ... + 10^2 = 385
    The square of the sum of the first ten natural numbers is,

    (1 + 2 + ... + 10)^2 = 55^2 = 3025
    Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025  385 = 2640.

    Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum."""
    s = (100 * (100 + 1)) // 2
    brute_force_s = sum(range(101))
    assert s == brute_force_s
    result = sum(x * (s - x) for x in range(101))
    brute_force_result = sum(range(101)) ** 2 - sum(x ** 2 for x in range(101))
    assert result == brute_force_result
    return result


def p007():
    """By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

    What is the 10 001st prime number?"""
    bound = 1
    p = primes(bound)
    while len(p) < 10001:
        bound *= 2
        p = primes(bound)
    return p[10000]


def p008():
    """Find the greatest product of five consecutive digits in the 1000-digit number.

    73167176531330624919225119674426574742355349194934
    96983520312774506326239578318016984801869478851843
    85861560789112949495459501737958331952853208805511
    12540698747158523863050715693290963295227443043557
    66896648950445244523161731856403098711121722383113
    62229893423380308135336276614282806444486645238749
    30358907296290491560440772390713810515859307960866
    70172427121883998797908792274921901699720888093776
    65727333001053367881220235421809751254540594752243
    52584907711670556013604839586446706324415722155397
    53697817977846174064955149290862569321978468622482
    83972241375657056057490261407972968652414535100474
    82166370484403199890008895243450658541227588666881
    16427171479924442928230863465674813919123162824586
    17866458359124566529476545682848912883142607690042
    24219022671055626321111109370544217506941658960408
    07198403850962455444362981230987879927244284909188
    84580156166097919133875499200524063689912560717606
    05886116467109405077541002256983155200055935729725
    71636269561882670428252483600823257530420752963450"""
    n_str = ''.join(x.strip() for x in p008.__doc__.splitlines()[2:])
    assert len(n_str) == 1000
    n_list = [int(x) for x in n_str]
    return max(reduce(op.mul, n_list[i:i + 5]) for i in range(1000))


def p009():
    """A Pythagorean triplet is a set of three natural numbers, a  b  c, for which,

    a^2 + b^2 = c^2
    For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

    There exists exactly one Pythagorean triplet for which a + b + c = 1000.
    Find the product abc."""
    for a, b in it.combinations_with_replacement(range(1, 501), 2):
        c = 1000 - a - b
        if a ** 2 + b ** 2 == c ** 2:
            break
    return a * b * c


def p010():
    """The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

    Find the sum of all the primes below two million."""
    return sum(primes(2 * 10 ** 6))


def p011():
    """In the 20x20 grid below, four numbers along a diagonal line have been marked in red.

    08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
    49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
    81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
    52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
    22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
    24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
    32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
    67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
    24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
    21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
    78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
    16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
    86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
    19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
    04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
    88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
    04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
    20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
    20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
    01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48

    The product of these numbers is 26 * 63 * 78 * 14 = 1788696.

    What is the greatest product of four adjacent numbers in any direction (up, down, left, right, or diagonally) in the 20x20 grid?"""
    a = np.array([[int(x) for x in row.split()] for row in p011.__doc__.splitlines()[2:-4]])
    assert a.shape == (20, 20)
    n = 4
    verticals = reduce(op.mul, (a[i:i + a.shape[0] - n + 1, :] for i in range(n)))
    horizontals = reduce(op.mul, (a[:, i:i + a.shape[1] - n + 1] for i in range(n)))
    diagonals = reduce(op.mul, (a[i:i + a.shape[0] - n + 1, i:i + a.shape[1] - n + 1] for i in range(n)))
    antidiagonals = reduce(op.mul, (a[i:i + a.shape[0] - n + 1, n - i - 1:a.shape[1] - i] for i in range(n)))
    return int(max(verticals.max(), horizontals.max(), diagonals.max(), antidiagonals.max()))


def p012():
    """The sequence of triangle numbers is generated by adding the natural numbers. So the 7th triangle number would be 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28. The first ten terms would be:

    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

    Let us list the factors of the first seven triangle numbers:

     1: 1
     3: 1,3
     6: 1,2,3,6
    10: 1,2,5,10
    15: 1,3,5,15
    21: 1,3,7,21
    28: 1,2,4,7,14,28
    We can see that 28 is the first triangle number to have over five divisors.

    What is the value of the first triangle number to have over five hundred divisors?"""
    for n in it.count():
        if len(divisors(triangle(n))) > 500:
            return triangle(n)


def p013():
    """Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.

    37107287533902102798797998220837590246510135740250
    46376937677490009712648124896970078050417018260538
    74324986199524741059474233309513058123726617309629
    91942213363574161572522430563301811072406154908250
    23067588207539346171171980310421047513778063246676
    89261670696623633820136378418383684178734361726757
    28112879812849979408065481931592621691275889832738
    44274228917432520321923589422876796487670272189318
    47451445736001306439091167216856844588711603153276
    70386486105843025439939619828917593665686757934951
    62176457141856560629502157223196586755079324193331
    64906352462741904929101432445813822663347944758178
    92575867718337217661963751590579239728245598838407
    58203565325359399008402633568948830189458628227828
    80181199384826282014278194139940567587151170094390
    35398664372827112653829987240784473053190104293586
    86515506006295864861532075273371959191420517255829
    71693888707715466499115593487603532921714970056938
    54370070576826684624621495650076471787294438377604
    53282654108756828443191190634694037855217779295145
    36123272525000296071075082563815656710885258350721
    45876576172410976447339110607218265236877223636045
    17423706905851860660448207621209813287860733969412
    81142660418086830619328460811191061556940512689692
    51934325451728388641918047049293215058642563049483
    62467221648435076201727918039944693004732956340691
    15732444386908125794514089057706229429197107928209
    55037687525678773091862540744969844508330393682126
    18336384825330154686196124348767681297534375946515
    80386287592878490201521685554828717201219257766954
    78182833757993103614740356856449095527097864797581
    16726320100436897842553539920931837441497806860984
    48403098129077791799088218795327364475675590848030
    87086987551392711854517078544161852424320693150332
    59959406895756536782107074926966537676326235447210
    69793950679652694742597709739166693763042633987085
    41052684708299085211399427365734116182760315001271
    65378607361501080857009149939512557028198746004375
    35829035317434717326932123578154982629742552737307
    94953759765105305946966067683156574377167401875275
    88902802571733229619176668713819931811048770190271
    25267680276078003013678680992525463401061632866526
    36270218540497705585629946580636237993140746255962
    24074486908231174977792365466257246923322810917141
    91430288197103288597806669760892938638285025333403
    34413065578016127815921815005561868836468420090470
    23053081172816430487623791969842487255036638784583
    11487696932154902810424020138335124462181441773470
    63783299490636259666498587618221225225512486764533
    67720186971698544312419572409913959008952310058822
    95548255300263520781532296796249481641953868218774
    76085327132285723110424803456124867697064507995236
    37774242535411291684276865538926205024910326572967
    23701913275725675285653248258265463092207058596522
    29798860272258331913126375147341994889534765745501
    18495701454879288984856827726077713721403798879715
    38298203783031473527721580348144513491373226651381
    34829543829199918180278916522431027392251122869539
    40957953066405232632538044100059654939159879593635
    29746152185502371307642255121183693803580388584903
    41698116222072977186158236678424689157993532961922
    62467957194401269043877107275048102390895523597457
    23189706772547915061505504953922979530901129967519
    86188088225875314529584099251203829009407770775672
    11306739708304724483816533873502340845647058077308
    82959174767140363198008187129011875491310547126581
    97623331044818386269515456334926366572897563400500
    42846280183517070527831839425882145521227251250327
    55121603546981200581762165212827652751691296897789
    32238195734329339946437501907836945765883352399886
    75506164965184775180738168837861091527357929701337
    62177842752192623401942399639168044983993173312731
    32924185707147349566916674687634660915035914677504
    99518671430235219628894890102423325116913619626622
    73267460800591547471830798392868535206946944540724
    76841822524674417161514036427982273348055556214818
    97142617910342598647204516893989422179826088076852
    87783646182799346313767754307809363333018982642090
    10848802521674670883215120185883543223812876952786
    71329612474782464538636993009049310363619763878039
    62184073572399794223406235393808339651327408011116
    66627891981488087797941876876144230030984490851411
    60661826293682836764744779239180335110989069790714
    85786944089552990653640447425576083659976645795096
    66024396409905389607120198219976047599490197230297
    64913982680032973156037120041377903785566085089252
    16730939319872750275468906903707539413042652315011
    94809377245048795150954100921645863754710598436791
    78639167021187492431995700641917969777599028300699
    15368713711936614952811305876380278410754449733078
    40789923115535562561142322423255033685442488917353
    44889911501440648020369068063960672322193204149535
    41503128880339536053299340368006977710650566631954
    81234880673210146739058568557934581403627822703280
    82616570773948327592232845941706525094512325230608
    22918802058777319719839450180888072429661980811197
    77158542502016545090413245809786882778948721859617
    72107838435069186155435662884062257473692284509516
    20849603980134001723930671666823555245252804609722
    53503534226472524250874054075591789781264330331690"""
    numbers = [int(x.strip()) for x in p013.__doc__.splitlines()[2:]]
    return int(str(sum(numbers))[:10])


def p014():
    """The following iterative sequence is defined for the set of positive integers:

    n  n/2 (n is even)
    n  3n + 1 (n is odd)

    Using the rule above and starting with 13, we generate the following sequence:

    13  40  20  10  5  16  8  4  2  1
    It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

    Which starting number, under one million, produces the longest chain?

    NOTE: Once the chain starts the terms are allowed to go above one million."""
    return max(range(1, 10 ** 6), key=collatz_length)


def p015():
    """Starting in the top left corner of a 2x2 grid, there are 6 routes (without backtracking) to the bottom right corner.

    How many routes are there through a 20x20 grid?"""
    a = np.zeros((21, 21), dtype=int)
    a[0] = 1
    a[:, 0] = 1
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            if a[i, j] == 0:
                a[i, j] = a[i - 1, j] + a[i, j - 1]
    return int(a[-1, -1])


def p016():
    """2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

    What is the sum of the digits of the number 2^1000?"""
    return sum(int(x) for x in str(2 ** 1000))


def p017():
    """If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

    If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?


    NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage."""
    d = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
         7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve',
         13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
         17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
    prefixes = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty',
                7: 'seventy', 8: 'eighty', 9: 'ninety'}
    for n in range(20, 100):
        tens = n // 10
        units = n % 10
        d[n] = prefixes[tens] + ('-{}'.format(d[units]) if units else '')
    for n in range(100, 1000):
        hundreds = n // 100
        rest = n % 100
        d[n] = d[hundreds] + ' hundred' + (' and {}'.format(d[rest]) if rest else '')
    d[1000] = 'one thousand'
    return sum(1 for word in d.values() for c in word if c not in '- ')


def p018():
    """By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

    3
    7 4
    2 4 6
    8 5 9 3

    That is, 3 + 7 + 4 + 9 = 23.

    Find the maximum total from top to bottom of the triangle below:

    75
    95 64
    17 47 82
    18 35 87 10
    20 04 82 47 65
    19 01 23 75 03 34
    88 02 77 73 07 63 67
    99 65 04 28 06 16 70 92
    41 41 26 56 83 40 80 70 33
    41 48 72 33 47 32 37 16 94 29
    53 71 44 65 25 43 91 52 97 51 14
    70 11 33 28 77 73 17 78 39 68 17 57
    91 71 52 38 17 14 91 43 58 50 27 29 48
    63 66 04 68 89 53 67 30 73 16 69 87 40 31
    04 62 98 27 23 09 70 98 73 93 38 53 60 04 23

    NOTE: As there are only 16384 routes, it is possible to solve this problem by trying every route. However, Problem 67, is the same challenge with a triangle containing one-hundred rows; it cannot be solved by brute force, and requires a clever method! ;o)"""
    d = [[int(n) for n in x.split()] for x in p018.__doc__.splitlines()[11:-2]]
    s = [[0] * len(r) for r in d]
    s[-1][:] = d[-1][:]
    r = len(d) - 2
    while r >= 0:
        for i in range(r + 1):
            s[r][i] = d[r][i] + max(s[r + 1][i], s[r + 1][i + 1])
        r -= 1
    return s[0][0]


def p019():
    """You are given the following information, but you may prefer to do some research for yourself.

    1 Jan 1900 was a Monday.
    Thirty days has September,
    April, June and November.
    All the rest have thirty-one,
    Saving February alone,
    Which has twenty-eight, rain or shine.
    And on leap years, twenty-nine.
    A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
    How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?"""
    d = dt.date(1901, 1, 1) + dt.timedelta(5)  # first sunday
    count = 0
    while d.year <= 2000:
        if d.day == 1:
            count += 1
        d += dt.timedelta(7)
    return count


def p020():
    """n! means n * (n - 1) * ... * 3 * 2 * 1

    For example, 10! = 10 * 9 * ... * 3 * 2 * 1 = 3628800,
    and the sum of the digits in the number 10! is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.

    Find the sum of the digits in the number 100!"""
    return sum(int(x) for x in str(math.factorial(100)))


def p021():
    """Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
    If d(a) = b and d(b) = a, where a != b, then a and b are an amicable pair and each of a and b are called amicable numbers.

    For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

    Evaluate the sum of all the amicable numbers under 10000."""
    result = 0
    for n in range(1, 10000):
        d = sum(divisors(n)[:-1])
        if d != n and sum(divisors(d)[:-1]) == n:
            result += n
    return result


def p022():
    """Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

    For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938  53 = 49714.

    What is the total of all the name scores in the file?"""
    with open(os.path.join(os.path.dirname(__file__), 'names.txt')) as f:
        names = sorted(ast.literal_eval(f.read()))
    return sum(sum(ord(c) - 64 for c in name) * i for i, name in enumerate(names, 1))


def p023():
    """A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

    A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum exceeds n.

    As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

    Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers."""
    abundant_numbers = [x for x in range(1, 28124) if sum(divisors(x)[:-1]) > x]
    Ns = set(range(1, 28124))
    ns = {x + y for x, y in it.combinations_with_replacement(abundant_numbers, 2)}
    return sum(Ns - ns)


def p024():
    """A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

    012   021   102   120   201   210

    What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?"""
    return int(''.join(str(n) for n in next(it.islice(it.permutations(range(10)), 10 ** 6 - 1, 10 ** 6))))


def p025():
    """The Fibonacci sequence is defined by the recurrence relation:

    Fn = Fn1 + Fn2, where F1 = 1 and F2 = 1.
    Hence the first 12 terms will be:

    F1 = 1
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 5
    F6 = 8
    F7 = 13
    F8 = 21
    F9 = 34
    F10 = 55
    F11 = 89
    F12 = 144
    The 12th term, F12, is the first term to contain three digits.

    What is the first term in the Fibonacci sequence to contain 1000 digits?"""
    fg = fib_gen()
    for i in it.count():
        if next(fg) >= 10 ** 999:
            break
    return i


def p026():
    """A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:

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

    Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part."""
    # from Fermat's little theorem, the period of the repeating decimal of 1 / p
    # is equal to the order of 10 modulo p.  If 10 is a primitive root modulo p,
    # the period is equal to p - 1; if not, the period is a factor of p - 1.
    return max(primes(1000)[4:], key=lambda x: multiplicative_order(10, x))


def p027():
    """Euler published the remarkable quadratic formula:

    n^2 + n + 41

    It turns out that the formula will produce 40 primes for the consecutive values n = 0 to 39. However, when n = 40, 402 + 40 + 41 = 40(40 + 1) + 41 is divisible by 41, and certainly when n = 41, 41^2 + 41 + 41 is clearly divisible by 41.

    Using computers, the incredible formula  n^2 - 79n + 1601 was discovered, which produces 80 primes for the consecutive values n = 0 to 79. The product of the coefficients, 79 and 1601, is 126479.

    Considering quadratics of the form:

    n^2 + an + b, where |a| < 1000 and |b| < 1000

    where |n| is the modulus/absolute value of n
    e.g. |11| = 11 and |-4| = 4
    Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n = 0."""
    max_count = 40
    max_ab = 1 * 41

    def f(n, a, b):
        return is_prime(n ** 2 + a * n + b)
    # b must be prime (consider n = 0)
    for b in primes(1000):
        # a must be odd (consider n = 1)
        for a in range(-999, 1000, 2):
            if all(f(x, a, b) for x in reversed(range(max_count))):
                while True:
                    if f(max_count + 1, a, b):
                        max_count += 1
                        max_ab = a * b
                    else:
                        break
    return max_ab


def p028():
    """Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

    21 22 23 24 25
    20  7  8  9 10
    19  6  1  2 11
    18  5  4  3 12
    17 16 15 14 13

    It can be verified that the sum of the numbers on the diagonals is 101.

    What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?"""
    def spiral_gen():
        n = 1
        yield n
        step = 2
        while True:
            for _ in range(4):
                n += step
                yield n
            step += 2
    g = spiral_gen()
    return sum(next(g) for x in range(1001 * 2 - 1))


def p029():
    """Consider all integer combinations of a^b for 2 <= a <= 5 and 2 <= b <= 5:

    2^2=4, 2^3=8, 2^4=16, 2^5=32
    3^2=9, 3^3=27, 3^4=81, 3^5=243
    4^2=16, 4^3=64, 4^4=256, 4^5=1024
    5^2=25, 5^3=125, 5^4=625, 5^5=3125
    If they are then placed in numerical order, with any repeats removed, we get the following sequence of 15 distinct terms:

    4, 8, 9, 16, 25, 27, 32, 64, 81, 125, 243, 256, 625, 1024, 3125

    How many distinct terms are in the sequence generated by ab for 2 <= a <= 100 and 2 <= b <= 100?"""
    return len({a ** b for a in range(2, 101) for b in range(2, 101)})


def p030():
    """Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

    1634 = 1^4 + 6^4 + 3^4 + 4^4
    8208 = 8^4 + 2^4 + 0^4 + 8^4
    9474 = 9^4 + 4^4 + 7^4 + 4^4
    As 1 = 1^4 is not a sum it is not included.

    The sum of these numbers is 1634 + 8208 + 9474 = 19316.

    Find the sum of all the numbers that can be written as the sum of fifth powers of their digits."""
    return sum(i for i in range(10, 9 ** 5 * 6) if i == sum(int(d) ** 5 for d in str(i)))


def p031():
    """In England the currency is made up of pound, P, and pence, p, and there are eight coins in general circulation:

    1p, 2p, 5p, 10p, 20p, 50p, 1P (100p) and 2P (200p).
    It is possible to make 2P in the following way:

    1P + 50p + 2 x 20p + 5p + 2p + 3 x 1p
    How many different ways can 2P be made using any number of coins?"""
    def ways(wallet=[], coins=(200, 100, 50, 20, 10, 5, 2, 1)):
        amount = sum(wallet)
        if amount == 200:
            return 1
        elif amount > 200:
            return 0
        else:
            smallest_coin = wallet[-1] if wallet else 200
            new_coins = coins[coins.index(smallest_coin):]
            return sum(ways(wallet + [c], new_coins) for c in new_coins)
    return ways()


def p032():
    """We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

    The product 7254 is unusual, as the identity, 39 x 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

    Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

    HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum."""
    pandigital_products = set()
    candidates = [n for n in range(2000) if '0' not in str(n) and unique_digits(n)]
    for k, n in enumerate(candidates):
        for m in candidates[k:]:
            s = set(str(n)) & set(str(m))
            if not s:
                mn = str(m * n)
                if '0' not in mn and unique_digits(mn) and set('123456789') - set(str(m) + str(n)) == set(mn):
                    pandigital_products |= {m * n}
    return sum(pandigital_products)


def p033():
    """The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

    We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

    There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

    If the product of these four fractions is given in its lowest common terms, find the value of the denominator."""
    nontrivial_curious_fractions = []
    for numerator in range(10, 100):
        for denominator in range(numerator + 1, 100):
            assert numerator / denominator < 1
            s = set(str(numerator)) & set(str(denominator)) - {'0'}
            if len(s) == 1:
                d = s.pop()
                try:
                    numerator_, denominator_ = int(str(numerator).strip(d)), int(str(denominator).strip(d))
                except ValueError:
                    # int('') called due to double digit coincidence
                    continue
                if numerator * denominator_ == numerator_ * denominator:
                    nontrivial_curious_fractions.append((numerator, denominator))
    assert len(nontrivial_curious_fractions) == 4
    prod_numerators = prod_denominators = 1
    for n, d in nontrivial_curious_fractions:
        prod_numerators *= n
        prod_denominators *= d
    return prod_denominators // gcd(prod_numerators, prod_denominators)


def p034():
    """145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

    Find the sum of all numbers which are equal to the sum of the factorial of their digits.

    Note: as 1! = 1 and 2! = 2 are not sums they are not included."""
    lookup = [math.factorial(n) for n in range(10)]
    return sum(n for n in range(10, math.factorial(9)) if sum(lookup[int(d)] for d in str(n)) == n)


def p035():
    """The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

    There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

    How many circular primes are there below one million?"""
    return sum(1 for p in primes(1000000) if all(int(str(p)[n:] + str(p)[:n]) in Primes for n in range(1, len(str(p)))))


def p036():
    """The decimal number, 585 = 1001001001 (binary), is palindromic in both bases.

    Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

    (Please note that the palindromic number, in either base, may not include leading zeros.)"""
    return sum(n for n in range(1000000) if palindrome(str(n)) and palindrome(str(bin(n))[2:]))


def p037():
    """The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

    Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

    NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes."""
    total = 0
    count = 0
    for n in it.count(11, 2):
        str_n = str(n)
        len_n = len(str_n)
        if n in Primes and all(int(str_n[k:]) in Primes and int(str_n[:k]) in Primes for k in range(1, len_n)):
            count += 1
            total += n
            if count == 11:
                return total


def p038():
    """Take the number 192 and multiply it by each of 1, 2, and 3:

    192 * 1 = 192
    192 * 2 = 384
    192 * 3 = 576
    By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

    The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

    What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?"""
    largest = 918273645
    for m in range(91, 10000):
        s = str(m) + str(2 * m)
        if '0' in s or not unique_digits(s):
            continue
        for n in it.count(3):
            s_ = str(n * m)
            if '0' in s_ or not unique_digits(s_ + s):
                break
            s += s_
        if set(s) == set('123456789'):
            largest = max(int(s), largest)
    return largest


def p039():
    """If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

    {20,48,52}, {24,45,51}, {30,40,50}

    For which value of p <= 1000, is the number of solutions maximised?"""
    squares = {n ** 2 for n in range(1, 501)}
    counter = collections.Counter()
    for a in range(1, 501):
        for b in range(a, 501):
            if a ** 2 + b ** 2 in squares:
                c = isqrt(a ** 2 + b ** 2)
                p = a + b + c
                if p <= 1000:
                    counter[p] += 1
    return counter.most_common(1)[0][0]


def p040():
    """An irrational decimal fraction is created by concatenating the positive integers:

    0.123456789101112131415161718192021...

    It can be seen that the 12th digit of the fractional part is 1.

    If dn represents the nth digit of the fractional part, find the value of the following expression.

    d1 * d10 * d100 * d1000 * d10000 * d100000 * d1000000"""
    s = '.'
    for i in it.count(1):
        s += str(i)
        if len(s) > 1000000:
            return reduce(op.mul, [int(s[10 ** d]) for d in range(7)], 1)


def p041():
    """We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

    What is the largest n-digit pandigital prime that exists?"""
    i = 9
    while i > 0:
        for t in it.permutations(''.join(str(d) for d in range(i, 0, -1)), i):
            n = int(''.join(t))
            if is_prime(n):
                return n
        else:
            i -= 1


def p042():
    """The nth term of the sequence of triangle numbers is given by, tn = n*(n+1)/2; so the first ten triangle numbers are:

    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

    By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.

    Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?"""
    with open(os.path.join(os.path.dirname(__file__), 'words.txt')) as f:
        words = ast.literal_eval(f.read())
    tri = set(it.takewhile(lambda t: t <= len(max(words, key=len)) * 26, triangles()))
    return sum(1 for word in words if sum(ord(c) - 64 for c in word) in tri)


def p043():
    """The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

    Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:

    d2d3d4=406 is divisible by 2
    d3d4d5=063 is divisible by 3
    d4d5d6=635 is divisible by 5
    d5d6d7=357 is divisible by 7
    d6d7d8=572 is divisible by 11
    d7d8d9=728 is divisible by 13
    d8d9d10=289 is divisible by 17

    Find the sum of all 0 to 9 pandigital numbers with this property."""
    hits = {1406357289}
    # d6 must be 0 or 5 in order for d4d5d6 to be divisble by 5.  but if d6 == 0,
    # then d6d7d8 == d7d8 can't be divisible by 11 since this implies d7 == d8
    # which is impossible for a pandigital number.  therefore d6 == 5.
    d6 = 5
    d678 = [x for x in range(500, 600) if x % 11 == 0 and unique_digits(x)]
    for n in d678:
        d7 = (n % 100) // 10
        d8 = n % 10
        for d9 in set(range(10)) - {d6, d7, d8}:
            if (100 * d7 + 10 * d8 + d9) % 13 == 0:
                for d10 in set(range(10)) - {d6, d7, d8, d9}:
                    if (100 * d8 + 10 * d9 + d10) % 17 == 0:
                        for d5 in set(range(10)) - {d6, d7, d8, d9, d10}:
                            if (100 * d5 + 10 * d6 + d7) % 7 == 0:
                                # d2d3d4 is even and hence d4 must be in '02468'
                                for d4 in set(range(0, 10, 2)) - {d5, d6, d7, d8, d9, d10}:
                                    for d3 in set(range(10)) - {d4, d5, d6, d7, d8, d9, d10}:
                                        # d345, and therefore also d3 + d4 + d5, must be divisible by 3
                                        if (d3 + d4 + d5) % 3 == 0:
                                            d1, d2 = set(range(10)) - {d3, d4, d5, d6, d7, d8, d9, d10}
                                            hit = sum(10 ** i * d for i, d in enumerate([d10, d9, d8, d7, d6, d5, d4, d3, d2, d1]))
                                            hits |= {hit}
                                            d2, d1 = d1, d2
                                            hit = sum(10 ** i * d for i, d in enumerate([d10, d9, d8, d7, d6, d5, d4, d3, d2, d1]))
                                            hits |= {hit}
    assert all(unique_digits(d) for d in hits)
    return sum(hits)


def p044():
    """Pentagonal numbers are generated by the formula, Pn = n * (3 * n - 1) / 2. The first ten pentagonal numbers are:

    1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...

    It can be seen that P4 + P7 = 22 + 70 = 92 = P8. However, their difference, 70 - 22 = 48, is not pentagonal.

    Find the pair of pentagonal numbers, Pj and Pk, for which their sum and difference are pentagonal and D = |Pk - Pj| is minimised; what is the value of D?"""
    for n in it.count(1):
        pn = pentagonal(n)
        lower_pentagonals = [pentagonal(i) for i in range(1, n)]
        for p in lower_pentagonals:
            if pn - p in Pentagonals and pn + p in Pentagonals:
                return pn - p


def p045():
    """Triangle, pentagonal, and hexagonal numbers are generated by the following formulae:

    Triangle    Tn = n(n+1)/2      1, 3, 6, 10, 15, ...
    Pentagonal  Pn = n(3n-1)/2     1, 5, 12, 22, 35, ...
    Hexagonal   Hn = n(2n-1)       1, 6, 15, 28, 45, ...
    It can be verified that T285 = P165 = H143 = 40755.

    Find the next triangle number that is also pentagonal and hexagonal."""
    for n in it.count(285 + 1):
        Tn = triangle(n)
        if Tn in Pentagonals and Tn in Hexagonals:
            return Tn


def p046():
    """It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

     9 =  7 + 2 * 1^2
    15 =  7 + 2 * 2^2
    21 =  3 + 2 * 3^2
    25 =  7 + 2 * 3^2
    27 = 19 + 2 * 2^2
    33 = 31 + 2 * 1^2

    It turns out that the conjecture was false.

    What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?"""
    bound = 10
    while True:
        candidates = np.ones(bound, dtype=bool)
        # strike out the evens, and the trivial solution
        candidates[::2] = False
        candidates[1] = False
        for p in primes(bound):
            for i in it.count():
                try:
                    candidates[p + 2 * i * i] = False
                except IndexError:
                    break
        if any(candidates):
            return int(candidates.argmax())
        else:
            bound *= 2


def p047():
    """The first two consecutive numbers to have two distinct prime factors are:

    14 = 2 x 7
    15 = 3 x 5

    The first three consecutive numbers to have three distinct prime factors are:

    644 = 2^2 x 7 x 23
    645 = 3 x 5 x 43
    646 = 2 x 17 x 19.

    Find the first four consecutive integers to have four distinct prime factors. What is the first of these numbers?"""
    n = 4
    for i in it.count():
        if all(len(set(factorise(i + k))) == n for k in range(n)):
            return i


def p048():
    """The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.

    Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000."""
    return int(str(sum(i ** i for i in range(1, 1001)))[-10:])


def p049():
    """The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

    There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

    What 12-digit number do you form by concatenating the three terms in this sequence?"""
    primes4 = set(primes(10000)[len(primes(1000)):])  # 4-digit primes
    for p in primes4:
        p1 = 3330 + p
        p2 = 3330 + p1
        if p1 in primes4 and p2 in primes4:
            if sorted(str(p1)) == sorted(str(p2)) == sorted(str(p)):
                if p != 1487:
                    return p2 + p1 * 10 ** 4 + p * 10 ** 8


def p050():
    """The prime 41, can be written as the sum of six consecutive primes:

    41 = 2 + 3 + 5 + 7 + 11 + 13
    This is the longest sum of consecutive primes that adds to a prime below one-hundred.

    The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.

    Which prime, below one-million, can be written as the sum of the most consecutive primes?"""
    p = primes(10 ** 6)
    set_p = set(p)
    # first find an upper bound on n
    n = 1
    while sum(p[:n]) < 10 ** 6:
        n += 1
    while True:
        for i in it.count():
            sum_p = sum(p[i:n + i])
            if sum_p < 10 ** 6:
                if sum_p in set_p:
                    return sum_p
            else:
                break
        n -= 1


def p051():
    """By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

    By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.

    Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family."""
    # it will never make sense to replace the last digit, because of even numbers

    def replacements(n, positions):
        template = list(str(n))
        for position in positions:
            template[position] = '?'
        for d in string.digits[1 if 0 in positions else 0:]:
            yield int(''.join(template).replace('?', d))

    some_primes = primes(10 ** 6)  # primes below 10 million
    set_primes = set(some_primes)
    for p in some_primes:
        n = len(str(p))
        for i in range(1, n):
            for indices in it.combinations(range(n - 1), i):
                hits = [x for x in replacements(p, indices) if x in set_primes]
                if len(hits) == 8:
                    return sorted(hits)[0]


def p052():
    """It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

    Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits."""
    for n in it.count(1):
        strs = [str(i * n) for i in range(1, 7)]
        if len(set([''.join(sorted(s)) for s in strs])) == 1:
            return n


if __name__ == '__main__' and 1:

    import doctest
    doctest.testmod()

    parser = ap.ArgumentParser("Wim's project euler progress")
    parser.add_argument('--all', action='store_true')
    parser.add_argument('ids', type=int, nargs='*', default=[])
    args = parser.parse_args()

    ids = args.ids or range(1, 501)
    for problem_number in ids:
        problem = locals().get('p{:03d}'.format(problem_number))
        next_problem = locals().get('p{:03d}'.format(problem_number + 1))
        if problem is not None and (next_problem is None or args.all or args.ids):
            t0 = time.time()
            answer = problem()
            dt = time.time() - t0
            if answer is not None and type(answer) != int:
                print('result {} is instance {}, expected int'.format(problem_number, type(answer)))
            print('problem {:3d}: {} ({:.02f} s)'.format(problem_number, answer, dt))
