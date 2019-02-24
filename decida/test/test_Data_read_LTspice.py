#! /usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm
from decida.FrameNotebook import FrameNotebook

test_dir = decida.test.test_dir()

fn = FrameNotebook()
d = Data(verbose=False)

d.read_nutmeg(test_dir + "data/LTspice/binary/ac.raw")
XYplotm(fn.new_page("bin_ac"), command=[d, "frequency DB(V(vout1)) PH(V(vout1))"], title="AC analysis", xaxis="log", ymin=-60.0, ymax=0.0)

d.read_nutmeg(test_dir + "data/LTspice/ascii/ac.raw")
XYplotm(fn.new_page("asc_ac"), command=[d, "frequency DB(V(vout1)) PH(V(vout1))"], title="AC analysis", xaxis="log", ymin=-60.0, ymax=0.0)

fn.wait()
