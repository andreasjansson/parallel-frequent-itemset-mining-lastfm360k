#!/usr/bin/env python

import sys
import math

def main():
    artist_counts = []
    for line in sys.stdin:
        artist, count = line.strip().split('\t')
        count = int(count)
        artist_counts.append((artist, count))

    n_groups = 100
    n_artists = len(artist_counts)
    n_per_group = n_artists / float(n_groups)
    offset = 0

    # output lines in the form GROUP\tARTIST1\tARTIST2\tARTIST3, etc., for each group
    for i in xrange(0, n_groups):
        next_offset = offset + n_per_group + 1
        group = artist_counts[int(offset) : int(next_offset)]
        offset = next_offset
        artist_count_strings = ['%s:%d' % (artist, count) for artist, count in group]
        print '%s\t%s' % (i, '\t'.join(artist_count_strings))

if __name__ == '__main__':
    main()
