#!/usr/bin/env python

import sys

for line in sys.stdin:
    try:
        user, artist_mbid, artist, plays = line.strip().split('\t')
        print '%s\t%s' % (user, artist)
    except ValueError:
        pass
