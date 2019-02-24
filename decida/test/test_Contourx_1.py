#!/usr/bin/env python
import math
import decida
from decida.Contourx import Contourx

xmin, xmax, ymin, ymax, nx, ny, nc = -20, 20, -20, 20, 41, 41, 41
def zfunction(x, y) :
    return math.pow(
        (math.pow((x-10.0),2.0)+math.pow(y,2.0))*
        (math.pow((x+10.0),2.0)+math.pow(y,2.0)), 0.25
    )
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
