#!/usr/bin/env python3

import collections

import numpy as np
import aocd

YEAR = 2024
DAY = 1


def sim(a, b):
    counter = collections.Counter(b)
    return sum(i * counter[i] for i in a)


def main():
    data = """3   4
4   3
2   5
1   3
3   9
3   3
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = np.array([tuple(map(int, l.split())) for l in data.split('\n') if l])

    answer = np.sum(np.abs(np.diff(np.sort(inlist, axis=0), axis=1)))
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = sim(inlist[:, 0], inlist[:, 1])
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
