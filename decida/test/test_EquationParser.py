#!/usr/bin/env python
from __future__ import print_function
from decida.EquationParser import EquationParser

eqns = [
    "z =V(1)",
    "z =V(1)* sin(x+3.0)*ID(mp2)",
    "z = V(1) * sin ( x + 3.0 ) * ID(mp2)",
    "z =!(time <= V(1)) && (sin(x) < ID(mp2))",
    "z = (!(time <= V(1))) && (sin(x) < ID(mp2))",
    "z = + a - b",
    "z = V(1)*2",
    "z = (x < - 23) || (x > 23)",
    "z = (x *  -23) + (x * 23)",
    "z = time <= V(1) && sin(x) < ID(mp2)",
]
cols = ["V(1)", "ID(mp2)", "x", "y1"]
for eqn in eqns :
    ep = EquationParser(eqn, varlist=cols, debug=False)
    lines = ep.parse()
    ivars = ep.ivars()
    del ep
    print("=" * 72)
    print("equation : ", eqn)
    print("ivars    : ", ivars)
    for line in lines :
        print("   %s" % (line))
