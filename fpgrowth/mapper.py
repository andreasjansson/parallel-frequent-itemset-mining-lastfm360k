#!/usr/bin/env python

import sys
from collections import namedtuple

def main():
    group_list = read_group_list()

    for line in sys.stdin:
        user, artists = line.strip().split('\t', 1)
        artists = artists.split('\t')
        artists = sorted(artists, key=lambda artist: group_list[artist].count, reverse=True)
        artist_groups = [group_list[artist].artist for artist in artists]
        emitted_groups = set()

        for i, group_id in reversed(list(enumerate(artist_groups))):
            if group_id not in emitted_groups:
                emitted_groups.add(group_id)
                print '%s\t%s' % (group_id, '\t'.join(artists[:(i + 1)]))

ArtistCount = namedtuple('ArtistCount', ['artist', 'count'])

def read_group_list():
    artist_groups = {}

    with open('/home/andreas/scratch/group_list.tsv', 'r') as f:
        for line in f:
            group_id, artist_counts = line.strip().split('\t', 1)
            artist_counts = artist_counts.split('\t')
            for artist_count in artist_counts:
                artist, count = artist_count.rsplit(':', 1)
                artist_groups[artist] = ArtistCount(int(group_id), int(count))

    return artist_groups

main()
