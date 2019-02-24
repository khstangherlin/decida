#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.DataViewm import DataViewm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/sspice/ascii/dc.raw")
d.set("i(vd) = - i(vd)")
DataViewm(data=d, command=[["vd i(vd)"],["vd i(vb)", "yaxis=\"log\""]])
