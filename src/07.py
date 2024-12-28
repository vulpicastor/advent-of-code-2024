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
DAY = 7


def concat(a, b):
    return int(str(a) + str(b))


def rpn_eval(tokens):
    stack = []
    for token in tokens:
        match token:
            case func if callable(func):
                stack.append(func(stack.pop(), stack.pop()))
            case int() | float():
                stack.append(token)
    return stack


def calibrate(res, args, op_list=[op.add, op.mul]):
    argc = len(args)
    rargs = list(reversed(args))
    # print(res)
    for ops in itertools.product(op_list, repeat=argc-1):
        tokens = rargs.copy()
        tokens.extend(ops)
        # print(tokens)
        if (test_res := rpn_eval(tokens)[0]) == res:
            return True
        # print(test_res)
    return False

# def simple_eval(args, ops):
#     ops[0](args[0], args[1])


def main():
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l.split(': ') for l in data.split('\n') if l]  # noqa: F841
    tests = []
    for v, l in inlist:
        tests.append((int(v), [int(x) for x in l.split()]))
    

    # print(rpn_eval([1, 2, 3, op.mul, op.add]))
    # print(rpn_eval([1, 2, op.mul, 3, op.add]))

    answer = sum([v for v, t in tests if calibrate(v, t)])
    print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    new_op_list = [op.add, op.mul, concat]
    answer = sum([v for v, t in tests if calibrate(v, t, new_op_list)])
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
