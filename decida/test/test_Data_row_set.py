#!/usr/bin/env python
import decida
import decida.test
from decida.Data import Data

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/data.csv")
d.show()
d.row_set(3, [2.1, 3.3])
d.show()
