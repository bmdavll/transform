#!/usr/bin/env python3

import sys, random

def compose(seq, count, dupes=None):
    assert dupes is None or count <= len(seq) * dupes

    s = ''
    for i in range(count):
        while True:
            choice = random.choice(seq)
            if dupes is None:
                break
            elif choice == '':
                break
            elif s.count(choice) < dupes:
                break
        s += choice
        if not s and random.random() < 0.01:
            break
    return s


chars = []
length = 42

for i in range(8):
    chars.append('')

for i in range(94):
    chars.append(chr(ord(' ')+i))

if len(sys.argv) == 1:
    count = 1
else:
    count = int(sys.argv[1])

for i in range(count):
    print(compose(chars, length, 4))
