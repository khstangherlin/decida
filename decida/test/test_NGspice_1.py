#!/usr/bin/env python
import decida
import decida.test
from decida.NGspice import NGspice

test_dir = decida.test.test_dir()
NGspice(cktfile=test_dir + "data/hartley.ckt", xcol="time", ycols="v(c)")
