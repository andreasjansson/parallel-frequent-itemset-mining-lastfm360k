#!/usr/bin/env python

import sys
import math
import random

N_GROUPS = 1000

def main():
    artist_counts = []
    for line in sys.stdin:
        artist, count = line.strip().split('\t')
        group = random.randint(0, N_GROUPS - 1)
        print '%d\t%s:%d' % (group, artist, int(count))

if __name__ == '__main__':
    main()
