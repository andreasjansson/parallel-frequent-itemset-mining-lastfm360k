#!/usr/bin/env python

import sys
import simplejson as json

def output(artist, patterns):
    json_patterns = []
    for artists, support in patterns.iteritems():
        json_patterns.append({'artists': list(artists), 'support': support})
    print artist, json.dumps(json_patterns)

current_artist = None
patterns = {}

for line in sys.stdin:
    try:
        artist, pattern_raw = line.strip().split('\t')
        pattern = json.loads(pattern_raw)
    except (ValueError, json.JSONDecodeError) as e:
        sys.stderr.write('reporter:counter:errors,reduce_input_line_invalid,1')
        continue

    if artist != current_artist:
        if current_artist is not None:
            output(current_artist, patterns)
        current_artist = artist
        patterns = {}
        
    artists = frozenset(pattern['artists'])
    if artists not in patterns or patterns[artists] < pattern['support']:
        patterns[artists] = pattern['support']

if current_artist:
    output(current_artist, patterns)
