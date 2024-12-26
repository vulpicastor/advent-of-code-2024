#!/usr/bin/env python3

# ruff: noqa: F401
import collections
import functools
import io
import itertools
import operator as op
import re
import timeit

import numpy as np
import aocd

YEAR = 2024
DAY = 4


def xmas_diag_iter(grid):
    nrow = len(grid)
    max_diag = max(0, nrow - 4)
    for k in range(-max_diag, max_diag + 1):
        diag = np.diagonal(grid, k)
        yield ''.join(diag)
        yield ''.join(diag[::-1])


def xmas_row_iter(grid):
    for r in grid:
        yield ''.join(r)
        yield ''.join(r[::-1])


def xmas_iter(grid):
    yield from xmas_row_iter(grid)
    yield from xmas_row_iter(grid.T)
    yield from xmas_diag_iter(grid)
    yield from xmas_diag_iter(grid[:, ::-1])


def count_xmas(grid):
    num_xmas = 0
    for s in xmas_iter(grid):
        num_xmas += len(re.findall('XMAS', s))
    return num_xmas


X_MAS = np.array([list('M S'), list(' A '), list('M S')])
X_MASES = [X_MAS, X_MAS[:, ::-1], X_MAS.T, X_MAS.T[::-1]]
X_MAS_MASK = ~(X_MAS == ' ')


def scan_grid(grid):
    size = len(grid)
    for i, j in itertools.product(range(1, size-1), repeat=2):
        yield grid[i - 1:i + 2, j - 1:j + 2]


def x_mas_match(grid, pattern, mask):
    return np.all(((grid == pattern) & mask) == mask)


def count_x_mas(grid):
    num_x_mas = 0
    for subgrid in scan_grid(grid):
        for x_mas in X_MASES:
            num_x_mas += x_mas_match(subgrid, x_mas, X_MAS_MASK)
    return num_x_mas


def main():
    data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [list(l) for l in data.split('\n') if l]  # noqa: F841
    grid = np.array(inlist)

    answer = count_xmas(grid)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # print(X_MAS)
    # print(X_MASES)
    # print(X_MAS_MASK)
    answer = count_x_mas(grid)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
