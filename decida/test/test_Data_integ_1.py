#! /usr/bin/env python
from builtins import range
import numpy
import decida
import decida.test
from decida.Data      import Data
from decida.DataViewm import DataViewm

def integ_trap_dcd(d, zcol, ycol, xcol):
    d.set("$zcol = integ($ycol, $xcol)")

def integ_trap_npy(d, zcol, ycol, xcol):
    xvals = d.get(xcol)
    yvals = d.get(ycol)
    d.set("$zcol = 0.0")
    nrows = d.nrows()
    z = 0.0
    d.set_entry(0, zcol, z)
    for row in range(1, nrows) :
        z=numpy.trapz(yvals[0:row+1], x=xvals[0:row+1])
        d.set_entry(row, zcol, z)

def integ_trap_man(d, zcol, ycol, xcol):
    d.set("$zcol = 0.0")
    nrows = d.nrows()
    z = 0.0
    d.set_entry(0, zcol, z)
    for row in range(1, nrows) :
        xl = d.get_entry(row-1, xcol)
        xh = d.get_entry(row,   xcol)
        yl = d.get_entry(row-1, ycol)
        yh = d.get_entry(row,   ycol)
        z = z + 0.5*(yh+yl)*(xh-xl)
        d.set_entry(row, zcol, z)

d = Data()
times = decida.range_sample(0.0, 10.0, step=0.1)
d.read_inline("time", times)
freq = 0.25
d.set("y       = sin(2*pi*$freq*time)")
d.set("y_integ = (1.0-cos(2*pi*$freq*time))/(2*pi*$freq)")
integ_trap_dcd(d, "y_trap_dcd", "y", "time")
integ_trap_npy(d, "y_trap_npy", "y", "time")
integ_trap_man(d, "y_trap_man", "y", "time")
DataViewm(data=d, command=[["time y_integ y_trap_dcd y_trap_npy y_trap_man"]])
