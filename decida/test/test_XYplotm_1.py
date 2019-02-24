#!/usr/bin/env python
from __future__ import print_function
import profile
import pstats
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm

test_dir = decida.test.test_dir()

d = Data()
d.read(test_dir + "data/LTspice/ascii/ac.raw")
profile.run("XYplotm(command=[d, \"frequency DB(V(vout1))\"])", "stats.pro")
p = pstats.Stats("stats.pro")
p.strip_dirs().sort_stats('time').print_stats()
