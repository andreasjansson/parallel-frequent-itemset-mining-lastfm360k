#!/usr/bin/env python

import sys
import heapq
from collections import defaultdict

def main():

    current_group_id = None
    transactions = []
#    for line in sys.stdin:
    for line in open('/home/andreas/scratch/mapped.tsv', 'r'):
        group_id, artists = line.strip().split('\t', 1)
        artists = artists.split('\t')

        if group_id != current_group_id:
            if current_group_id is not None:
                output_frequent_itemsets(transactions)
                transactions = []
            current_group_id = group_id

        transactions.append(artists)

    if current_group_id is not None:
        output_frequent_itemsets(transactions)

def output_frequent_itemsets(transactions):        
    fp_tree, header_table = build_fp_tree(transactions)
    frequent_itemsets = mine_frequent_itemsets(fp_tree, header_table)
#    for artists, support in frequent_itemsets:
#        print '%s\t%d\t%s' % ('None', support, '\t'.join(artists))

class Node(object):
    def __init__(self, artist, support, parent, children):
        self.artist = artist
        self.support = support
        self.parent = parent
        self.children = children

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

def mine_frequent_itemsets(fp_tree, header_table):
    import ipdb; ipdb.set_trace()

main()
