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
DAY = 1





def main():
    data = """
"""
    data = aocd.get_data(day=DAY, year=YEAR)
    inlist = [l for l in data.split('\n') if l]  # noqa: F841

    # answer = 
    # print(answer)
    # aocd.submit(answer, part='a', day=DAY, year=YEAR)

    # answer = 
    # print(answer)
    # aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
