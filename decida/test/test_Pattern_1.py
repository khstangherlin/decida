#!/usr/bin/env python
from __future__ import print_function
from builtins import zip
from decida.Pattern import Pattern

p = Pattern(delay=4e-9, start_at_first_bit=True, edge=0.1e-9)
pwl = p.prbs(length=50)
print("t v")
for t,v in zip(pwl[0::2], pwl[1::2]) :
    print(t, v)
