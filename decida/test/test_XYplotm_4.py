#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/sspice/binary/tr.raw")
d.show()
xyplot=XYplotm(None, command=[d, "time v(cint) v(osc) v(q_2)"])
