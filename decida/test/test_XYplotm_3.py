#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/sspice/ascii/dc.raw")
XYplotm(None, command=[d, "v(d) i(vd)"])
