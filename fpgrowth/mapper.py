#!/usr/bin/env python

import sys
from collections import namedtuple
import contextlib
import subprocess

def main(group_file_name):
    group_list = read_group_list(group_file_name)

    for line in sys.stdin:
        user, artists = line.strip().split('\t', 1)

        # artists will be in the format ARTIST1\tARTIST2\tARTIST3, etc.
        artists = artists.split('\t')

        # sort artists by count in descending order
        artists = sorted(artists, key=lambda artist: group_list[artist].count, reverse=True)

        artist_groups = [group_list[artist].group for artist in artists]
        emitted_groups = set()

        for i, group_id in reversed(list(enumerate(artist_groups))):
            if group_id not in emitted_groups:
                emitted_groups.add(group_id)
                print '%s\t%s' % (group_id, '\t'.join(artists[:(i + 1)]))

GroupCount = namedtuple('GroupCount', ['group', 'count'])

def read_group_list(group_file_name):
    group_list = {}

    with open_file(group_file_name) as f:
        for line in f:
            group_id, artist_counts = line.strip().split('\t', 1)
            artist_counts = artist_counts.split('\t')
            for artist_count in artist_counts:
                artist, count = artist_count.rsplit(':', 1)
                group_list[artist] = GroupCount(int(group_id), int(count))

    return group_list

@contextlib.contextmanager
def open_file(filename):
    if group_file_name.startswith('hdfs://'):
        proc = subprocess.Popen(['hadoop', 'dfs', '-cat', filename], stdout=subprocess.PIPE)
        def iterator():
            while True:
                line = proc.stdout.readline()
                if line == '':
                    break
                yield line
        yield iterator()
    else:
        f = open(filename, 'r')
        try:
            yield f
        finally:
            f.close()
    

if __name__ == '__main__':

    # get GROUP_FILE_NAME argument
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: ./mapper GROUP_FILE_NAME')
        exit(1)
    group_file_name = sys.argv[1].strip()
    sys.argv.pop(1)

    main(group_file_name)
