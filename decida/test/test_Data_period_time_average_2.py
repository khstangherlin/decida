#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.DataViewm import DataViewm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/lcosc.tr.col")
dx = d.period_time_average("time", "ivdd", period=70e-12)
DataViewm(data=dx, command=[["time avg"]])
