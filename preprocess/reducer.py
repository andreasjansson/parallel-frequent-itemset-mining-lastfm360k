#!/usr/bin/env python

import sys

def main():

    current_user = None
    artists = set()

    for line in sys.stdin:
        user, artist = line.strip().split('\t')

        if current_user != user:
            if current_user is not None:
                output(current_user, artists)
                artists = set()
            current_user = user

        artists.add(artist)

    if current_user is not None:
        output(current_user, artists)

def output(user, artists):
    print '%s\t%s' % (user, '\t'.join(artists))

if __name__ == '__main__':
    main()
