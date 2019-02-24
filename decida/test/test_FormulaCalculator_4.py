#!/usr/bin/env python
from decida.FormulaCalculator import FormulaCalculator

fc = FormulaCalculator(None,
    title="fixed rate mortgage calculator",
    par_specs = [
        ["principal",     "Principal",     "$",  100000,  "payment"],
        ["years",         "Years",         "y",  30,      "payment"],
        ["rate",          "Rate",          "%",  8.00,    "payment"],
        ["payments_year", "Payments/Year", "",   12,      "payment"],
        ["payment",       "Payment",       "$",  733.76,  "principal"],
    ],
    recalc_specs = [
        ["payment",  """
             a            = 1.0e-2*rate/payments_year
             N            = 1.0*payments_year*years
             per_thousand = 1.0e+3*a/(1-pow(1+a, -N))
             payment      = 1.0e-3*principal*per_thousand
        """],
        ["principal", """
             a            = 1.0e-2*rate/payments_year
             N            = 1.0*payments_year*years
             per_thousand = 1.0e+3*a/(1-pow(1+a,-N))
             principal    = 1.0e+3*payment/per_thousand
       """],
    ]
)
