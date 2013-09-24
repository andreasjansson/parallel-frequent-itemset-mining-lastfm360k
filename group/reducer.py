#!/usr/bin/env python

import sys

def main():
    current_group = None
    current_artists = []

    for line in sys.stdin:
        group, artist = line.strip().split('\t')

        if group != current_group:
            if current_group is not None:
                output(current_group, current_artists)
                current_artists = []
            current_group = group

        current_artists.append(artist)

    if current_group is not None:
        output(current_group, current_artists)

def output(group, artists):
    print '%s\t%s' % (group, '\t'.join(artists))

if __name__ == '__main__':
    main()
