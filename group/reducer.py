#!/usr/bin/env python

import sys

def main():
    current_group = None
    current_artists = []

    for line in sys.stdin:
        group, artists = line.strip().split('\t', 1)
        artists = artists.split('\t')

        if group != current_group:
            if current_group is not None:
                output(current_group, current_artists)
                current_artists = []
            current_group = group

        current_artists.extend(artists)

    if current_group is not None:
        output(current_group, current_artists)

def output(group, artists):
    print '%s\t%s' % (group, '\t'.join(artists))

if __name__ == '__main__':
    main()
