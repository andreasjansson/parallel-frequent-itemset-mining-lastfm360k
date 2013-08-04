#!/usr/bin/env python

import sys
import simplejson as json

for line in sys.stdin:
    try:
        _, pattern_raw = line.strip().split('\t')
        pattern = json.loads(pattern_raw)
    except (ValueError, json.JSONDecodeError) as e:
        sys.stderr.write('reporter:counter:errors,map_input_line_invalid,1')
        continue

    for artist in pattern['artists']:
        print ('%s\t%s' % (artist, pattern_raw)).encode('utf-8')
