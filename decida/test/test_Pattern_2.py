#!/usr/bin/env python
from __future__ import print_function
from builtins import range
from decida.Pattern import Pattern

#--------------------------------
# check duty-cycle of the pattern
#--------------------------------
def duty(pattern) :
    n = len(pattern)
    pat = [int(x) for x in pattern]
    s0 = float(sum(pat))
    D = {}
    for v in range(1, n) :
        s = sum([pat[j]*pat[(j+v)%n] for j in range(n)])
        d = float(s)/s0
        D[d] = 1
    ds = list(D.keys())
    if len(ds) != 1 :
        return(-1)
    return(ds[0])

p = Pattern(format="binary")
for size in range(2, 8) :
    pattern = p.prbs(size)
    d=duty(pattern)
    print(size, d, pattern)
