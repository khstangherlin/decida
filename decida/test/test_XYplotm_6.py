#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/LTspice/ascii/ac.raw")
XYplotm(None, command=[d, "frequency DB(V(vout1)) PH(V(vout1)) DB(V(vout2)) PH(V(vout2)) DB(V(vout3)) PH(V(vout3))"], title="AC analysis", xaxis="log", ymin=-60.0, ymax=0.0)
