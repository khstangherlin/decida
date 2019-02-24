#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.MessageDialog import MessageDialog

test_dir = decida.test.test_dir()
d=Data()
d.read_ssv(test_dir + "data/lcosc.tr.col")
d.set("ivdd=-ivdd")
xcol = "time"
ycol = "ivdd"
yrms = d.rms(xcol, ycol)
yavg = d.time_average(xcol, ycol)
ymin = d.min(ycol)
ymax = d.max(ycol)
yave = d.mean(ycol)
ymed = d.median(ycol)
yvar = d.var(ycol)
ystd = d.std(ycol)
report = decida.interpolate("""
    Signal=$ycol time=$xcol:
    RMS                     $yrms
    Time-average            $yavg
    Minimum                 $ymin
    Maximum                 $ymax
    Median                  $ymed
    Average                 $yave
    Variance                $yvar
    Standard deviation      $ystd
""")
MessageDialog(title="statistics", message=report)
