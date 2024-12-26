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
DAY = 3


def match_mul(s):
    res = re.findall(r'mul\(([0-9]+),([0-9]+)\)', s)
    return [tuple(int(n) for n in m) for m in res]


def mul_sum(res):
    return np.sum(np.prod(np.array(res), axis=1))


def match_mul_cond(s):
    res = re.findall(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", s)
    return res


def exec_mul_cond(res):
    enabled = True
    total = 0
    for l in res:
        match l:
            case 'do()':
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if not enabled:
                    continue
                m = re.match(r'mul\(([0-9]+),([0-9]+)\)', l)
                a, b = m.group(1, 2)
                total += int(a) * int(b)
            # case _:
            #     raise ValueError(f'Unmatched case: {l}')
    return total
                


def main():
    data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
    data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    data = aocd.get_data(day=DAY, year=YEAR)
    # inlist = [l for l in data.split('\n') if l]  # noqa: F841

    res = match_mul(data)
    answer = mul_sum(res)
    print(res)
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    res = match_mul_cond(data)
    print(res)
    answer = exec_mul_cond(res)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
