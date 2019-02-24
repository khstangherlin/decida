#!/usr/bin/env python
from __future__ import print_function
from decida.SelectionDialog import SelectionDialog

guispecs = [
   ["check", "Checkbox Selections", [
       ["CHECK_KEY0", "select check 0", True],
       ["CHECK_KEY1", "select check 1", True],
       ["CHECK_KEY2", "select check 2", False],
   ]],
   ["radio", "Radiobox Selections", "RADIO_KEY", "RADIO_VAL0", [
       ["select radio 0", "RADIO_VAL0"],
       ["select radio 1", "RADIO_VAL1"],
       ["select radio 2", "RADIO_VAL2"],
   ]],
]
if True :
    guispecs.append(
       ["entry", "Entry Selections", [
           ["ENTRY_KEY0", "entry 0", 1.2],
           ["ENTRY_KEY1", "entry 1", 2.2],
           ["ENTRY_KEY2", "entry 2", 2.3],
           ["ENTRY_KEY21", "entry 2", 2.3],
           ["ENTRY_KEY22", "entry 2", 2.3],
           ["ENTRY_KEY23", "entry 2", 2.3],
           ["ENTRY_KEY24", "entry 2", 2.3],
           ["ENTRY_KEY25", "entry 2", 2.3],
           ["ENTRY_KEY26", "entry 2", 2.3],
           ["ENTRY_KEY27", "entry 2", 2.3],
           ["ENTRY_KEY28", "entry 2", 2.3],
           ["ENTRY_KEY29", "entry 2", 2.3],
           ["ENTRY_KEY30", "entry 2", 2.3],
           ["ENTRY_KEY31", "entry 2", 2.3],
           ["ENTRY_KEY32", "entry 2", 2.3],
           ["ENTRY_KEY33", "entry 2", 2.3],
           ["ENTRY_KEY34", "entry 2", 2.3],
           ["ENTRY_KEY35", "entry 2", 2.3],
       ]])
sd = SelectionDialog(title="Selection Dialog", guispecs=guispecs)
V = sd.go()

for key in V :
    print("V[%s] = %s" % (key,  V[key]))
