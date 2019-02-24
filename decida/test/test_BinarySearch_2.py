#!/usr/bin/env python
from __future__ import print_function
from decida.BinarySearch import BinarySearch

def funct(x) :
    a, b, c = 1.0, -4.0, 2.0
    y = a*x*x + b*x + c
    return y

bs = BinarySearch(
     low=1.0, high=2.0, min_value=-10, max_value=3,
     min_delta=1e-6, bracket_step=0.1
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
