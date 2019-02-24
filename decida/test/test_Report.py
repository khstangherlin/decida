#! /usr/bin/env python
from builtins import range
from decida.Report import Report

rpt = Report("example.report", verbose=True)
rpt.user()
rpt.date()
rpt.header("time vscl")
for i in range(0, 20):
    t = i*1e-3/20
    v = 1.2 + 2.4*t + 840.0*t*t
    rpt.report(t, v)
