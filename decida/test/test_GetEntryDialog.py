#!/usr/bin/env python
from __future__ import print_function
from decida.GetEntryDialog import GetEntryDialog

ge = GetEntryDialog(title="GetEntry Dialog", message="comment characters", initialvalue="#")
c = ge.go()

print("c = ", c)
