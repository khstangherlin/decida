#!/usr/bin/env python
import os
import decida
import decida.test
from decida.NGspice import NGspice

test_dir = decida.test.test_dir()
os.environ["NGSPICE_INPUT_DIR"] = test_dir

netlist = """\
* mosfet char
vd d 0 1.0
vg g 0 1.0
mn d g 0 0 nmos L=1e-6 W=2e-6 AD=0.2e-12 AS=0.2e-12 PD=2.2e-6 PS=2.2e-6
.dc vd 0 1 .01    vg 0 1 .1
.save I(vd) V(d) V(g)
.include "data/130nm_bulk.inc"
.end
"""

NGspice(netlist=netlist, xcol="v(d)", ycols="i(vd)")
