#!/usr/bin/env python
from decida.FormulaCalculator import FormulaCalculator

fc = FormulaCalculator(None,
    title="Integrated resistor",
    par_specs = [
        ["r",   "Resistance",       "ohms",         1000, "l"],
        ["rho", "Sheet Resistance", "ohms/square",   200, "r"],
        ["dw",  "delta W",          "um",           0.02, "r"],
        ["dl",  "delta L",          "um",          -0.10, "r"],
        ["l",   "length",           "um",           10.0, "r"],
        ["w",   "width",            "um",            1.0, "l"],
    ],
    recalc_specs = [
        ["l", "l = 1.0*r*(w-dw)/rho + dl"],
        ["r", "r = 1.0*rho*(l-dl)/(w-dw)"],
    ]
)
