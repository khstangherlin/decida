#! /usr/bin/env python
from __future__ import print_function
from decida.Itemizer import Itemizer

procs = ["TT", "SS", "FF"]
vdds  = [0.9, 1.0, 1.1]
temps = [0, 25, 100]
ix = Itemizer(procs, vdds, temps, tag="%s.V_%s.T_%s")
for proc, vdd, temp in ix :
    tag = ix.tag()
    print(tag, proc, vdd, temp)
