#! /usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm
from decida.FrameNotebook import FrameNotebook

test_dir = decida.test.test_dir()

fn = FrameNotebook(tab_location="right")
d = Data()

d.read_nutmeg(test_dir + "data/NGspice/binary/tr.raw")
d.edit()
XYplotm(fn.new_page("(mat)bin_tr"), command=[d, "time v(c) v(x) v(z)"], title="TR analysis", ymin=-10, ymax=20)
XYplotm(fn.new_page("(xmat)bin_tr"), command=[d, "time v(c) v(x) v(z)"], title="TR analysis", ymin=-10, ymax=20, use_matplotlib=False)

d.read_nutmeg(test_dir + "data/NGspice/binary/dc.raw")
d.edit()
d.set("i(vd) = -i(vd)")
XYplotm(fn.new_page("(mat)asc_dc"), command=[d, "v(d) i(vd)"], title="DC analysis", ymin=0, ymax=70e-6)
XYplotm(fn.new_page("(xmat)asc_dc"), command=[d, "v(d) i(vd)"], title="DC analysis", ymin=0, ymax=70e-6, use_matplotlib=False)

fn.wait()
