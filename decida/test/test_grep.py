#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.grep import grep

test_dir = decida.test.test_dir()
output = grep("Plotname", test_dir + "data/sspice/ascii/dc.raw")
print(output)
