#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.Data import Data

test_dir = decida.test.test_dir()
d = Data()
d.read(test_dir + "data/data.csv")
d.show()

d.sort("freq")
d.show()

d1 = d.dup()

f3 = d.get_entry(3, "freq")
print("freq(3) = ", f3)
d.set_entry(3, "freq", f3*3)
d.show()

col = d1.unique_name("M")
d1.append(col)
d1.set("$col = wc")
print(col, "index = ", d1.index(col))
d1.show()

d1.insert(col, "wc2", "wc3")
d1.name(col, "wc1")
d1.set("point = index")
d1.show()

wcs = d1.get("wc1")
print("wcs = ", wcs)

d.become(d1)
d.show()

d1 = Data()
d1.read_inline("cpf", wcs)
d1.set("cpf = cpf*23")

d.append_data(d1)
d.delete("wc2", "wc3")
d.show()

d.filter("freq < 4.01")
d.show()

d1 = d.dup()
d1.row_append_data(d)
d1.sort("freq")
d1.show()

freqs = d1.unique("freq")
print("unique freqs = ", freqs)

d1.select("cpf", "freq")
d1.set("df = del(freq) != 0")
d1.show()

rows = d1.find_rows_where_equal("df", 1)
print("rows = ", rows)

d1.filter("df == 1")
d1.row_append(2)
d1.row_set(-1, [3, 3, 3])
d1.row_set(-2, [6, 6, 6])
r3 = d1.row_get(3)
print("row 3 = ", r3)
d1.show()
