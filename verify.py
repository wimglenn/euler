#!/usr/bin/env python3
import json
import time
import euler

with open('./euler/my_answers.json') as f:
    d = json.load(f)

t0 = time.time()
for i in range(1, 58):
    fname = f'p{i:03d}'
    __import__('euler.' + fname)
    m = getattr(euler, fname)
    assert getattr(m, 'result', None) == d[fname], fname
    print(fname, m.result)
