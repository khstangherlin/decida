#!/usr/bin/env python
from __future__ import print_function
import math
from decida.BinarySearch import BinarySearch

def funct(x) :
    y = math.log(x) - 1.0
    return y

bs = BinarySearch(
     low=0.5, high=2.0, min_value=0.1, max_value=10,
     min_delta=1e-6, bracket_step=0.1, find_max=False
)

bs.start()
while not bs.is_done() :
    x=bs.value()
    f=funct(x)
    success = (f >= 0)
    print("%-10s: x=%-18s y=%-18s %-5s" % (bs.mode(), x, f, success))
    bs.update(success)

print()
print("x = ", bs.last_success())
