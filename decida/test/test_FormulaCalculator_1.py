#!/usr/bin/env python
from decida.FormulaCalculator import FormulaCalculator

fc = FormulaCalculator(None,
    title="L-C oscillator",
    par_specs = [
        ["L",    "Inductance",  "pH", 1000.0, "f"],
        ["C",    "Capacitance", "pF",  25.00, "f"],
        ["freq", "Frequency",   "GHz",  1.00, "L"],
    ],
    recalc_specs = [
        ["f", "freq = 1e3/(2*pi*sqrt(L*C))"],
        ["L", "L    = 1e6/(C*pow(2*pi*freq, 2))"],
        ["C", "C    = 1e6/(L*pow(2*pi*freq, 2))"],
    ]
)
