#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.Data import Data
from decida.Fitter import Fitter
from decida.DataViewm import DataViewm

test_dir = decida.test.test_dir()

d=Data()
d.read(test_dir + "data/icp_tr_diff.report")
#       dicp_mod = a0 + a1*sign(dt)*(1-(1+(abs(dt/u0))^x0)/(1+(abs(dt/u1))^x1))
ftr=Fitter(
    """
        t1 = a1*sign(dt)
        num=1+abs(dt/u0)^x0
        den=1+abs(dt/u1)^x1
        dicp_mod = a0 + t1*(1-num/den)
    """,
    """
        a0 -3.77e-6         lower_limit=-1e-5  upper_limit=1e-5
        a1 6e-3     include lower_limit=1e-8   upper_limit=1
        u0 2.2e-10  include lower_limit=1e-11
        u1 2.1e-10  include lower_limit=1e-11
        x0 1.03     include lower_limit=1.0
        x1 1.03     include lower_limit=1.0
    """,
    meast_col="dicp",
    model_col="dicp_mod",
    error_col="residual",
    residual="relative",
    data=d
)
ftr.fit()

print(ftr.par_values())

DataViewm(data=d, command=[["dt residual"], ["dt dicp dicp_mod"]])
