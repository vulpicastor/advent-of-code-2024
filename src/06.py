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
import tqdm

YEAR = 2024
DAY = 6


STEP = [
    np.array([-1,  0]),
    np.array([ 0,  1]),
    np.array([ 1,  0]),
    np.array([ 0, -1]),
]


def guard_step(grid, pos, direction):
    new_direction = direction
    while grid[tuple(new_pos := pos + STEP[new_direction])]:
        # grid[tuple(new_pos := pos + STEP[direction])]:
        new_direction += 1
        new_direction %= 4
        # new_pos = pos + STEP[direction]
        # return new_pos, direction
    return new_pos, new_direction


def sim_guard(grid, start):
    visited = np.zeros_like(grid, dtype=np.int64)
    pos = np.array(start, copy=True)
    max_coords = np.array(grid.shape)
    direction = 0
    visited[tuple(pos)] = 1
    while True:
        # np.all(pos >= 0) and np.all(pos < max_coords):
        pos, direction = guard_step(grid, pos, direction)
        visited[tuple(pos)] += 1
        if np.any((next_pos := pos + STEP[direction]) < 0) or np.any(next_pos >= max_coords):
            break
    return visited


def detect_loop(grid, start):
    visited = np.zeros_like(grid, dtype=np.int8)
    pos = np.array(start, copy=True)
    max_coords = np.array(grid.shape)
    direction = 0
    visited[tuple(pos)] &= 1 << direction
    while True:
        # np.all(pos >= 0) and np.all(pos < max_coords):
        pos, direction = guard_step(grid, pos, direction)
        if visited[tuple(pos)] & (1 << direction):
            return True
        visited[tuple(pos)] |= 1 << direction
        if np.any((next_pos := pos + STEP[direction]) < 0) or np.any(next_pos >= max_coords):
            return False


def count_obstructions(grid, start, visited):
    test_grid = grid.copy()
    max_row, max_col = grid.shape
    num_obs = 0
    # print(np.where(visited > 0))
    for i, j in tqdm.tqdm(zip(*np.where(visited > 0))):
    # for i in range(max_row):
    #     for j in range(max_col):
        # if grid[i, j]:
        #     continue
        if start[0] == i and start[1] == j:
            continue
        test_grid[:] = grid
        test_grid[i, j] = True
        num_obs += detect_loop(test_grid, start)
    return num_obs


def main():
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = np.array([list(l) for l in data.split('\n') if l])  # noqa: F841
    # print(inlist)
    grid = ~(inlist != '#')
    start = np.array(np.where(inlist == '^')).reshape(2)
    # print(grid, start)

    visited = sim_guard(grid, start)
    answer = np.sum(visited > 0)
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = count_obstructions(grid, start, visited)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
