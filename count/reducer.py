#!/usr/bin/env python

import sys

current_artist = None
current_count = 0
for line in sys.stdin:
    artist, count = line.strip().split('\t')
    count = int(count)

    if current_artist != artist:
        if current_artist is not None:
            print '%s\t%d' % (current_artist, current_count)
            current_count = 0
        current_artist = artist

    current_count += count

if current_artist is not None:
    print '%s\t%d' % (current_artist, current_count)
