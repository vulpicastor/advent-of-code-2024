#!/usr/bin/env python3

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
    # Identify safe pairs.
    safe_diff_inc = (1 <= diff) & (diff <= 3)
    safe_diff_dec = (-3 <= diff) & (diff <= -1)
    len_diff = len(diff)
    if ((num_safe_diff_inc := np.sum(safe_diff_inc)) == len_diff
        or (num_safe_diff_dec := np.sum(safe_diff_dec)) == len_diff):
        # All pairs are safe.
        return True
    if num_safe_diff_inc < len_diff - 2 and num_safe_diff_dec < len_diff - 2:
        # Impossible to resolve > 2 unsafe pairs by removing one number.
        return False
    if num_safe_diff_dec > num_safe_diff_inc:
        # Coerce the sequence to be increasing.
        diff = -diff
        idx, = np.where(~safe_diff_dec)
    else:
        idx, = np.where(~safe_diff_inc)
    if len(idx) == 2:
        if idx[1] - idx[0] > 1:
            # Non-adjacent unsafe pairs cannot be resolved.
            return False
        if (1 <= diff[idx[0]] + diff[idx[1]] <= 3):
            # Removing one number merges unsafe pairs into a safe one.
            return True
        return False
    if idx == len(diff) - 1 or idx == 0:
        # First or last item can always be removed to make a sequence safe.
        return True
    if (1 <= diff[idx] + diff[idx + 1] <= 3
        or 1 <= diff[idx - 1] + diff[idx] <= 3):
        # Removing one number resolves the unsafe pair.
        return True
    return False


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
    print(answer)
    aocd.submit(np.sum(answer), part='a', day=DAY, year=YEAR)

    answer = [safe2(l) for l in inlist]
    print(answer)
    aocd.submit(np.sum(answer), part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
