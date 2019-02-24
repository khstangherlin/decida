#!/usr/bin/env python
from __future__ import print_function
from decida.spice_value import spice_value

nums = "1.23G 1A 1FF 1MEG 1.2M 23K".split()
for num in nums:
    print(num, spice_value(num))
