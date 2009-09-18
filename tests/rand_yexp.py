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
        if not s and random.random() < 0.08:
            break
    return s


flags = [ '', '', 'c', 'd', 's' ]
chars = [ '', '', '', '', '',
          '+-0', '1-9', 'A-H', 'E', 'L-P', 'M', 'O', 'O', 'R', 'S', 'W-Z',
          'h-k', 'h', 'i', 'l-o', 'n', 'v', '[-]', ' -,', '<', '>', '\\n' ]
repl  = [ '', '', '', '', '',
          '+-0', 'A-C', 'L-M', 'e-l', 'f', 'g', 'a', 's', 't',
          '[-]', ':-@', '{-~', '_', '|', '\\n' ]
length = 8

if len(sys.argv) == 1:
    count = 1
else:
    count = int(sys.argv[1])

for i in range(count):
    s = 'y/'
    s += compose(chars, length, 4)
    s += '/'
    s += compose(repl, length, 3)
    s += '/'
    s += ''.join(random.sample(flags, 2))
    print(s)
