#!/usr/bin/env python

import sys

current_user = None
artists = set()

for line in sys.stdin:
    user, artist = line.strip().split('\t')

    if current_user != user:
        if current_user is not None:
            print '%s\t%s' % (user, '\t'.join(artists))
            artists = set()
        current_user = user

    artists.add(artist)

if current_user is not None:
    print '%s\t%s' % (user, '\t'.join(artists))
