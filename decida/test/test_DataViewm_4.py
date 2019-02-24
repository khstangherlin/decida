#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.DataViewm import DataViewm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/sspice/binary/tr.raw")
DataViewm(data=d, command=[["time v(cint) v(osc)", "ymin=0, ymax=4"],  ["time v(q_2)"]])
