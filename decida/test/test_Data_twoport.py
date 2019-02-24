#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/spars.col")
d.twoport_StoY("Sdd11", "Sdd12", "Sdd21", "Sdd22", "Ydd11", "Ydd12", "Ydd21", "Ydd22")
d.twoport_YtoZ("Ydd11", "Ydd12", "Ydd21", "Ydd22", "Zdd11", "Zdd12", "Zdd21", "Zdd22")
d.twoport_YtoH("Ydd11", "Ydd12", "Ydd21", "Ydd22", "Hdd11", "Hdd12", "Hdd21", "Hdd22")
d.twoport_HtoY("Hdd11", "Hdd12", "Hdd21", "Hdd22", "Yx11",  "Yx12",  "Yx21",  "Yx22")
d.twoport_ZtoY("Zdd11", "Zdd12", "Zdd21", "Zdd22", "Y11",   "Y12",   "Y21",   "Y22")
d.twoport_YtoS("Y11",   "Y12",   "Y21",   "Y22",   "S11",   "S12",   "S21",   "S22")

cmd1 = []
cmd2 = []
for par in (
    ("Ydd11", "Yx11"), ("Ydd12", "Yx12"), ("Ydd21", "Yx21"), ("Ydd22", "Yx22"),
    ("Ydd11", "Y11"), ("Ydd12", "Y12"), ("Ydd21", "Y21"), ("Ydd22", "Y22"),
    ("Sdd11", "S11"), ("Sdd12", "S12"), ("Sdd21", "S21"), ("Sdd22", "S22"),
) :
    p1, p2 = par
    for ri in ("REAL", "IMAG") :
        col = "ERROR_%s(%s)" % (ri, p1)
        d.set("$col = $ri($p1) - $ri($p2)")
        cmd1.extend([d, "freq %s" % (col)])
        cmd2.extend([d, "freq %s(%s) %s(%s)" % (ri, p1, ri, p2)])

XYplotm(command=cmd1, xaxis="log", wait=False)
XYplotm(command=cmd2, xaxis="log")
