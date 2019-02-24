#!/usr/bin/env python
import math
import decida
from decida.Data import Data
from decida.XYplotm import XYplotm

d = Data()
npts, xmin, xmax = 10000, 0, 10
x_data = decida.range_sample(xmin, xmax, num=npts)
y_data = []
for x in x_data :
    y_data.append(math.sin(x*10))
d.read_inline("X", x_data, "Y", y_data)
XYplotm(command=[d, "X Y"])
