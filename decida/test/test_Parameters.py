#!/usr/bin/env python
from decida.Parameters import Parameters

L      = 146.575e-12
Co     = 241.50e-15
Cu     = 118.94e-15
C1     = 23.14e-15
C2     = 27.00e-15
Rat    = 0.25
nCx    = 1
#-------------------------------------------------------------------------
# specs:
# name, initial_value, include,
#     lower_limited, upper_limited, lower_limit, upper_limit
#-------------------------------------------------------------------------
parobj = Parameters(specs=(
   ("L" , L , True, True, False, 0.0, 0.0),
   ("Co", Co, True, True, False, 0.0, 0.0),
   ("Cu", Cu, True, True, False, 0.0, 0.0),
   ("C1", C1, True, True, False, 0.0, 0.0),
   ("C2", C2, True, True, False, 0.0, 0.0),
))

parobj.show("L")
parobj.modify("L", tied="1.0/(math.pow(2*math.pi*10e9,2)*Co)")
parobj.values([L,Co,Cu,C1,C2])
parobj.show("L")
