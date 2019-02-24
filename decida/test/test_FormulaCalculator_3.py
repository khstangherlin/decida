#!/usr/bin/env python
from decida.FormulaCalculator import FormulaCalculator

fc = FormulaCalculator(None,
    title="field mowing calculator",
    par_specs = [
        ["n",    "number of turns",  "",      43,  "t"],
        ["dr",   "swath",            "ft",     3,  "n"],
        ["s",    "speed",            "ft/s",   3,  "n"],
        ["t",    "total time",       "min",  100,  "n"],
    ],
    recalc_specs = [
        ["t", "t = n*(n+1)*(dr*pi)/(s*60.0)"],
        ["n", "n = sqrt(0.25 + (s*60.0*t)/(dr*pi)) - 0.5"],
    ]
)
