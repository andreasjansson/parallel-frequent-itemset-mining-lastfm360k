#!/usr/bin/env python

import sys

def main():
    for line in sys.stdin:
        user, artists = line.strip().split('\t', 1)
        artists = artists.split('\t')
        for artist in artists:
            print '%s\t%d' % (artist, 1)

if __name__ == '__main__':
    main()
