#! /usr/bin/env python
import decida
import decida.test
from decida.Data import Data
from decida.XYplotm import XYplotm
from decida.FrameNotebook import FrameNotebook

test_dir = decida.test.test_dir()

fn = FrameNotebook()
d = Data(verbose=False)

d.read_hspice(test_dir + "data/hspice/binary/tr.tr0")
XYplotm(fn.new_page("bin_tr"), command=[d, "TIME v(1) v(2)"])

d.read_hspice(test_dir + "data/hspice/binary/tr2.tr0")
XYplotm(fn.new_page("bin_tr2"), command=[d, "TIME v(1) v(2) v(3) v(4) v(5)"])

d.read_hspice(test_dir + "data/hspice/binary/ac.ac0")
XYplotm(fn.new_page("bin_ac"), command=[d, "HERTZ DB(v(2))"], xaxis="log")

d.read_hspice(test_dir + "data/hspice/ascii/tr.tr0")
XYplotm(fn.new_page("asc_tr"), command=[d, "TIME v(1) v(2)"])

d.read_hspice(test_dir + "data/hspice/ascii/tr2.tr0")
XYplotm(fn.new_page("asc_tr2"), command=[d, "TIME v(1) v(2) v(3) v(4) v(5)"])

d.read_hspice(test_dir + "data/hspice/ascii/ac.ac0")
XYplotm(fn.new_page("asc_ac"), command=[d, "HERTZ DB(v(2))"], xaxis="log")

fn.wait()
