#!/usr/bin/env python
import math
import decida
from decida.Contourx import Contourx

xmin, xmax, ymin, ymax, nx, ny, nc = -2, 2, -2, 2, 40, 40, 40
def zfunction(x, y) :
    tx = math.tan(x)
    ty = math.tanh(y)
    if tx == 0.0 :
        tx = 1e-12
    return math.atan(ty/tx)
xvalues = decida.range_sample(xmin, xmax, num=nx)
yvalues = decida.range_sample(ymin, ymax, num=ny)
zvalues = []
for x in xvalues :
    zx = list()
    for y in yvalues :
        z = zfunction(x, y)
        zx.append(z)
    zvalues.append(zx)
c=Contourx(None, xvalues=xvalues, yvalues=yvalues, zvalues=zvalues, num_contours=nc)
