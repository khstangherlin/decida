#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.Data import Data

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/spars.col")
print(d.names())
print(d.ncols())
print(d.nrows())
d.twin()
