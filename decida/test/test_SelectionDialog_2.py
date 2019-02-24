#!/usr/bin/env python
from __future__ import print_function
from decida.SelectionDialog import SelectionDialog

guispecs = [
    ["entry", "Entry Selections", [
        ["ENTRY_KEY0", "entry 0", 1.2],
    ]]
]
sd = SelectionDialog(title="Selection Dialog", guispecs=guispecs)
V = sd.go()

for key in V :
    print("V[%s] = %s" % (key,  V[key]))
