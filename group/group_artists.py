#!/usr/bin/env python

import sys
import math

artist_counts = []
for line in sys.stdin:
    artist, count = line.strip().split('\t')
    count = int(count)
    artist_counts.append((artist, count))

n_groups = 100
n_artists = len(artist_counts)
n_per_group = int(math.ceil(n_artists / float(n_groups)))
for i in xrange(0, n_groups):
    group = artist_counts[i * n_per_group : (i + 1) * n_per_group]
    artist_count_strings = ['%s:%d' % (artist, count) for artist, count in group]
    print '%s\t%s' % (i, '\t'.join(artist_count_strings))
