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
DAY = 2


def safe(l):
    diff = np.diff(l)
    if not (np.all(diff >= 0) or np.all(diff <= 0)):
        return False
    abs_diff = np.abs(diff)
    if np.any((abs_diff < 1) | (abs_diff > 3)):
        return False
    return True


def safe2(l):
    diff = np.diff(l)
    # abs_diff = np.abs(diff)
    # if np.all(diff >= 0) or np.all(diff <= 0):
    #     print('Condition: Monotonic')
    #     if np.any(abs_diff >= 3):
    #         print('Return: Gap too big')
    #         return False
    #     if np.sum(abs_diff < 1) >= 1:
    #         print('Return: Too many return')
    #         return False
    #     print('Return: Safe')
    #     return True
        # diff_in_bound = (abs_diff >= 1) & (abs_diff <= 3)
        # if np.all(diff_in_bound):
        #     return True
        # out_bound = ~diff_in_bound
        # total_out_bound = np.sum(out_bound)
        # if total_out_bound > 2:
        #     return False
        # where_out_bound = np.where(out_bound)
        # if total_out_bound == 2 and np.diff(where_out_bound) > 1:
        #         return False
        # fix = where_out_bound[0]
        # if fix >= len(diff) - 1:
        #     return False
        # fix_diff = np.sum(diff[fix:fix + 2])
        # if 1 <= fix_diff <= 3:
        #     return True
        # return
    safe_diff_inc = (1 <= diff) & (diff <= 3)
    safe_diff_dec = (-3 <= diff) & (diff <= -1)
    len_diff = len(diff)
    if ((num_safe_diff_inc := np.sum(safe_diff_inc)) == len_diff
        or (num_safe_diff_dec := np.sum(safe_diff_dec)) == len_diff):
        # print('Return SAFE: all safe')
        return True
    print(l)
    # unsafe_inc = num_safe_diff_inc < len_diff - 1
    # unsafe_dec = np.sum(safe_diff_dec) < len_diff - 1
    if num_safe_diff_inc < len_diff - 2 and num_safe_diff_dec < len_diff - 2:
        print('Return UNSAFE: Too many unsafe pairs')
        return False
    if num_safe_diff_dec > num_safe_diff_inc:
        print('Condition: Mostly decreasing, inverting')
        diff = -diff
        idx, = np.where(~safe_diff_dec)
    else:
        idx, = np.where(~safe_diff_inc)
    # elif (num_lt_zero := np.sum(diff < 0)) > 1 or (num_gt_zero := np.sum(diff > 0)) > 1:
    #     print('Condition Return: Too many non-monotonic pairs')
    #     return False
    # if num_gt_zero == 1:
    #     print('Condition: Mostly decreasing, inverting')
    #     diff = -diff
    # idx = np.where(diff < 0)
    print(f'Index of unsafe: {idx}')
    if len(idx) == 2:
        if idx[1] - idx[0] > 1:
            print('Return UNSAFE: Unsafe pairs not adjacent')
            return False
        if (1 <= diff[idx[0]] + diff[idx[1]] <= 3):
            print('Return SAFE: Unsafe pairs merged')
            return True
        print('Return UNSAFE: Unsafe pairs cannot be merged')
        return False
        # idx = idx[0]
    if idx == len(diff) - 1 or idx == 0:
        print('Return SAFE: only first or last pair unsafe')
        # Last item can always be removed.
        return True
    if (1 <= diff[idx] + diff[idx + 1] <= 3
        or 1 <= diff[idx - 1] + diff[idx] <= 3):
        # or 1 <= diff[idx + 1] + diff[idx + 2] <= 3):
        print('Return SAFE: Removing one element restores safety')
        return True
    print('Return UNSAFE: All checks failed')
    return False


def safe_scan(l):
    unsafe = False
    sign = 0
    for i, (p, n) in enumerate(itertools.pairwise(l)):
        diff = n - p
        if sign == 0:
            sign = np.sign(diff)
        else:
            pass
        if abs(diff) > 0:
            pass


def main():
    data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [np.array([int(i) for i in l.split()]) for l in data.split('\n') if l]

    answer = [safe(l) for l in inlist]
    # print(answer)
    # aocd.submit(np.sum(answer), part='a', day=DAY, year=YEAR)

    answer = [safe2(l) for l in inlist]
    print(answer)
    aocd.submit(np.sum(answer), part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
