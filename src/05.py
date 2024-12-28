#!/usr/bin/env python3

# ruff: noqa: F401
import collections
import functools
import io
import itertools
import operator as op
import re
import sys
import timeit

import numpy as np
import aocd

import tulun

YEAR = 2024
DAY = 5


# def check_order(nodes, dagraph):
#     forbidden = set()
#     for node in reversed(nodes):
#         if node in forbidden:
#             return False
#         forbidden |= dagraph.neigh(node)
#     return True
def check_order(nodes, dagraph):
    ancestors = set()
    for node in nodes:
        if (overlap := ancestors & dagraph.neigh(node)):
            print('Ancestor overlap:', overlap, 'at', node)
            return False
        ancestors.add(dagraph[node])
    return True 

def get_middle(l):
    return l[len(l) // 2]


def dfs_visit(graph, node, state):
    # print(parent)
    # print('DFS Visit:', node, 't =', state.t)
    for neigh in node:
        # print('Neighbor:', neigh)
        if neigh not in state.parent:
            state.parent[neigh] = node
            dfs_visit(graph, neigh, state)
        # if state.parent[neigh] is None:
        #     state.parent[neigh] = node
    state.t += 1
    state.finish[node] = state.t
    state.order.append(node)


# DfsState = collections.namedtuple('DfsState', ['t', 'finish', 'parent'])

class DfsState:

    def __init__(self, t=0, finish=None, parent=None, order=None):
        self.t = t
        self.finish = finish if finish is not None else dict()
        self.parent = parent if parent is not None else dict()
        self.order = order if order is not None else []


def dfs(graph, start=None):
    state = DfsState()
    if start is None:
        start = graph.values()
    for node in start:
        if node not in state.parent:
            # print(node)
            state.parent[node] = None
            dfs_visit(graph, node, state)
    return state


def find_roots(graph):
    reverse_graph = graph.reverse()
    print(reverse_graph)
    return [n for k, n in reverse_graph.items() if len(n) == 0]


def simple_toposort(nodes, graph):
    finish = dict()
    parent = dict()
    time = 0
    for node in nodes:
        # parent[node] = None
        if node not in parent:
            time = dfs_visit(node, nodes, graph, finish, parent, time)
    print([n.k for n in nodes])
    print({n.k: t for n, t in finish.items()})
    print({n.k: p.k if p is not None else None for n, p in parent.items()})
    nodes.sort(key=lambda k: finish[k])
    print([n.k for n in nodes])
    # print(nodes)
    print()
    return nodes


def make_graph(rules, node_list):
    return tulun.Digraph(edges=[(u, v) for u, v in rules if u in node_list and v in node_list])

    

def main():
    data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    data = aocd.get_data(day=DAY, year=YEAR)
    edges, node_list = data.split('\n\n')
    inlist = [[int(i) for i in l.split('|')] for l in edges.split('\n') if l]  # noqa: F841
    graph = tulun.Digraph(edges=inlist)
    print(graph)
    pages = [[int(i) for i in l.split(',')] for l in node_list.split('\n') if l]
    # print(pages)

    # ordered = [check_order(p, graph) for p in pages]
    # print(ordered)
    middles = [get_middle(p) for p in pages if check_order(p, graph)]
    # print(middles)
    answer = sum(middles)
    # print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # dfs_result = dfs(graph)
    # print(len(graph))
    # print({n.k: t for n, t in dfs_result.finish.items()})
    # print({n.k: p.k if p is not None else None for n, p in dfs_result.parent.items()})
    # print(dfs_result.parent)
    # print('Roots:', [n.k for n in find_roots(graph)])
    # return
    sort_incorrect = []
    for p in pages:
        if check_order(p, graph):
            continue
        # node_list = [graph[k] for k in p]
        small_graph = make_graph(inlist, p)
        dfs_finish = dfs(small_graph).finish
        p.sort(key=lambda k: -dfs_finish[small_graph[k]])
        # print(node_list)
        # sorted_pages = [n.k for n in node_list]
        print(p)
        assert check_order(p, graph)
        sort_incorrect.append(p)
        # sort_incorrect.append([n.k for n in simple_toposort(node_list, graph)])
    # print(sort_incorrect)
    middles = [get_middle(p) for p in sort_incorrect]
    answer = sum(middles)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
