"""
Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value, taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random bytes. The user would keep the encrypted message and the encryption key in different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key. If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message. The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using cipher.txt (right click and 'Save Link/Target As...'), a file containing the encrypted ASCII codes, and the knowledge that the plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the original text.
"""
from ast import literal_eval
from collections import Counter
from itertools import cycle
from pathlib import Path


def decrypt(cipher, key):
    decoded = (x ^ ord(k) for x, k in zip(cipher, cycle(key)))
    text = ''.join(chr(x) for x in decoded)
    return text


cipher = Path(__file__).parent.parent / 'data' / 'p059_cipher.txt'
numbers = literal_eval(cipher.read_text())
[(d0, _)] = Counter(numbers[0::3]).most_common(1)
[(d1, _)] = Counter(numbers[1::3]).most_common(1)
[(d2, _)] = Counter(numbers[2::3]).most_common(1)
key = "".join(chr(d ^ ord(" ")) for d in (d0, d1, d2))

txt = decrypt(numbers, key)
print(txt)
print(sum(ord(c) for c in txt))
