#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.SimulatorNetlist import SimulatorNetlist

test_dir = decida.test.test_dir()
s = SimulatorNetlist(test_dir + "sar_seq_dig.net", verbose=True,
    simulator="nanosim")
s["simulator"]="sspice"

print("subcircuits :")
print(s.get("subckts"))
print("instances :")
print(s.get("insts"))
print("capacitors:")
print(s.get("caps"))
print("resistors:")
print(s.get("ress"))
