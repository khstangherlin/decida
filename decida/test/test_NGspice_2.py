#!/usr/bin/env python
from decida.NGspice import NGspice

NGspice(ycols="i(v1)", xcol="v(1)", netlist="""
  * title
  v1 1 0 1
  r1 1 0 1
  .dc v1 0 1 .1
""")
