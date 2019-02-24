#!/usr/bin/env python
from decida.FormulaCalculator import FormulaCalculator

fc = FormulaCalculator(None,
    title="watering calculator",
    par_specs = [
        ["area",  "area",            "ft^2",     1000, "t"],
        ["gpm",   "gallons/minute",  "gal/min",   1.5, "t"],
        ["d",     "depth",           "in",        0.5, "t"],
        ["t",     "total time",      "hour",      1.5, "d"],
    ],
    recalc_specs = [
        ["t", """
            ft3_g = 231.0/1728.0
            t     = (1.0*area*(1.0*d/12))/(60.0*gpm*ft3_g)
        """],
        ["d", """
            ft3_g = 231.0/1728.0
            d     = (12.0*(t*60.0)*gpm*ft3_g)/area
        """],
    ],
)
