#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.SmithChartx import SmithChartx

test_dir = decida.test.test_dir()
d = Data()
d.read_sspar(test_dir + "data/port2.data")
SmithChartx(None, command=[d, "freq REAL(s33) IMAG(s33) REAL(s22) IMAG(s22) REAL(s11) IMAG(s11)"], symbols=["dot"])
