#! /usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.Data import Data
from decida.LevMar import LevMar
from decida.Parameters import Parameters
from decida.XYplotm import XYplotm

test_dir = decida.test.test_dir()

def lcfunc(parobj, dataobj):
    L  = parobj["L"]
    Co = parobj["Co"]
    Cu = parobj["Cu"]
    C1 = parobj["C1"]
    C2 = parobj["C2"]
    a2 = C2*16.0
    c2 = (C2-C1)*8.0
    b2 = (C2-C1)*24.0
    dataobj.set("Cc = (floor(vc/4.0)+fmod(vc,4)*0.25)*$Cu")
    dataobj.set("Cf = $a2 - $b2*vf + $c2*vf^2")
    dataobj.set("Ct = $Co + Cc + Cf")
    dataobj.set("fhat = 1.0/(2*pi*sqrt($L*Ct))")
    dataobj.set("residual = fhat - freq")

parobj = Parameters(specs=(
   ("L" , 2400e-12, False,  True, False, 0.0, 0.0),
   ("Co",  250e-15,  True,  True, False, 0.0, 0.0),
   ("Cu",   60e-15,  True,  True, False, 0.0, 0.0),
   ("C1",   23e-15,  True,  True, False, 0.0, 0.0),
   ("C2",   27e-15,  True,  True, False, 0.0, 0.0),
))

dataobj = Data()
dataobj.read(test_dir + "data/lcdata.col")

optobj = LevMar(lcfunc, parobj, dataobj,
    meast_col="freq", model_col="fhat", error_col="residual",
    quiet=False, debug=False
)
optobj.fit()
print(optobj.status())
print("parameters = ", list(parobj.values()))

XYplotm(command=[dataobj, "vf freq fhat"])
