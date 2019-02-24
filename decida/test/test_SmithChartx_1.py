#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.SmithChartx import SmithChartx

test_dir = decida.test.test_dir()
d = Data()
d.read_nutmeg(test_dir + "data/LTspice/ascii/ac.raw")
SmithChartx(None, command=[d, "frequency REAL(V(vout1)) IMAG(V(vout1))"])
