#!/usr/bin/env python

import sys

def main():
    current_artist = None
    current_count = 0
    for line in sys.stdin:
        artist, count = line.strip().split('\t')
        count = int(count)

        if current_artist != artist:
            if current_artist is not None:
                output(current_artist, current_count)
                current_count = 0
            current_artist = artist

        current_count += count

    if current_artist is not None:
        output(current_artist, current_count)

def output(artist, count):
    print '%s\t%d' % (artist, count)

if __name__ == '__main__':
    main()
