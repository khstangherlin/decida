#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.DataViewm import DataViewm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/LTspice/binary/ac.raw")
DataViewm(data=d, command=[["frequency DB(V(vout1)) PH(V(vout1))", "xaxis=\"log\""]])
