#!/usr/bin/env python

import sys
from collections import defaultdict, namedtuple
import itertools
import simplejson as json

MIN_SUPPORT = 5

def main():

    current_group_id = None
    transactions = []
    for line in sys.stdin:
        group_id, artists = line.strip().split('\t', 1)
        artists = artists.split('\t')

        if group_id != current_group_id:
            if current_group_id is not None:
                output(transactions)
                transactions = []
            current_group_id = group_id

        transactions.append(artists)

    if current_group_id is not None:
        output(transactions)

def output(transactions):        
    fp_tree, header_table = build_fp_tree(transactions)
    for pattern in fp_growth(fp_tree, header_table, None):
        print '%s\t%s' % ('_', pattern.to_json())

ArtistSupport = namedtuple('ArtistSupport', ['artist', 'support'])

class Node(object):
    def __init__(self, artist, support, parent, children):
        self.artist = artist
        self.support = support
        self.parent = parent
        self.children = children

    def get_artist_support(self):
        return ArtistSupport(self.artist, self.support)

    def get_single_prefix_path(self):
        path = []
        node = self
        while node.children:
            if len(node.children) > 1:
                return None
            path.append(node.children[0].get_artist_support())
            node = node.children[0]
        return path

    def clone(self, artist=None, support=None, parent=None, children=None):
        return Node(self.artist if artist is None else artist,
                    self.support if support is None else support,
                    self.parent if parent is None else parent,
                    self.children if children is None else children)

    def __str__(self):
        return self._to_string()

    def _to_string(self, level=0):
        return '%s%s:%s%s' % (('\n' + ' ' * level * 2) if level > 0 else '', self.artist, self.support, ''.join([c._to_string(level+1) for c in self.children]))


class Pattern(object):

    def __init__(self, items=None):
        if items:
            self.artists = set([x.artist for x in items])
            if len(self.artists) == len(items):
                self.support = min([x.support for x in items])
            else:
                deduped = defaultdict(int)
                for x in items:
                    deduped[x.artist] += x.support
                self.support = min(deduped.values())
        else:
            self.artists = []
            self.support = 0

    def __or__(self, other):
        if other is None:
            return self

        pattern = Pattern()
        pattern.artists = self.artists | other.artists
        pattern.support = min(self.support, other.support)
        return pattern

    def __len__(self):
        return len(self.artists)

    def __str__(self):
        return '(%s):%d' % (','.join(self.artists), self.support)

    def to_json(self):
        return json.dumps({'artists': list(self.artists), 'support': self.support})

def build_fp_tree(transactions):
    fp_tree = Node(None, None, None, [])
    header_table = defaultdict(list)
    for transaction in transactions:
        insert_transaction(fp_tree, header_table, transaction)
    return fp_tree, header_table

def insert_transaction(fp_tree, header_table, transaction):
    current_node = fp_tree
    for artist in transaction:
        found = False
        for child in current_node.children:
            if child.artist == artist:
                current_node = child
                current_node.support += 1
                found = True
                break
        if not found:
            new_node = Node(artist, 1, current_node, [])
            current_node.children.append(new_node)
            header_table[artist].append(new_node)
            current_node = new_node

def combinations(x):
    for i in xrange(1, len(x) + 1):
        for c in itertools.combinations(x, i):
            yield c

def fp_growth(tree, header_table, previous_pattern):

    single_path = tree.get_single_prefix_path()
    if single_path:
        for combination in combinations(single_path):
            pattern = Pattern(combination) | previous_pattern
            if pattern.support >= MIN_SUPPORT and len(pattern) > 1:
                yield pattern
    else:
        for artist, nodes in header_table.iteritems():
            pattern = Pattern(nodes) | previous_pattern

            if pattern.support >= MIN_SUPPORT:
                if len(pattern) > 1:
                    yield pattern

                conditional_tree, conditional_header_table = get_conditional_tree(nodes, tree)
                if conditional_tree:
                    for pattern in fp_growth(conditional_tree, conditional_header_table, pattern):
                        yield pattern

def get_conditional_tree(nodes, tree):

    child_list = defaultdict(set)
    header_table = defaultdict(set)
    shadowed = set()

    for node in nodes:

        leaf = node
        first_pass = True

        while node.parent is not None:
            parent = node.parent
            if hasattr(parent, '_shadow'):
                if parent.parent is not None:
                    parent._shadow.support += leaf.support
            else:
                if parent.parent is None:
                    parent._shadow = parent.clone(children=[])
                else:
                    parent._shadow = parent.clone(support=leaf.support, children=[])
                shadowed.add(parent)

            if first_pass:
                first_pass = False
            else:
                child_list[parent].add(node._shadow)
                header_table[node.artist].add(node._shadow)

            node = parent

    for node, children in child_list.iteritems():
        node._shadow.children = list(children)

    def set_parents(shadow):
        if shadow.children:
            for child in shadow.children:
                child.parent = shadow
                set_parents(child)

    shadow_tree = tree._shadow

    for node in shadowed:
        del node._shadow

    if not shadow_tree.children:
        return None, None

    set_parents(shadow_tree)

    return shadow_tree, header_table

if __name__ == '__main__':
    main()

def test():
    transactions = [
        ['f','a','c','d','g','i','m','p'],
        ['a','b','c','f','l','m','o'],
        ['b','f','h','j','o'],
        ['b','c','k','s','p'],
        ['a','f','c','e','l','p','m','n']
    ]
    f_list = defaultdict(int)
    for t in transactions:
        for x in t:
            f_list[x] += 1

    items = dict([(x, s) for x, s in f_list.items() if s >= MIN_SUPPORT])
    transactions = [sorted(filter(lambda x: x in items.keys(), t), key=lambda x: (items[x], x), reverse=True) for t in transactions]

    tree = build_fp_tree(transactions)

    return tree
