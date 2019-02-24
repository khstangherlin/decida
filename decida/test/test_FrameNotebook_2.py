#!/usr/bin/env python
import decida
import decida.test
from decida.Data          import Data
from decida.DataViewm     import DataViewm
from decida.FrameNotebook import FrameNotebook

test_dir = decida.test.test_dir()
files = ("icp_tr.report", "icp_tr.report")
nfiles = len(files)

fn = FrameNotebook(tab_location="right")
for ifile, filename in enumerate(files) :
    d = Data()
    d.read(test_dir + "data/" + filename)
    plt = "dt icp_final icp_expt"
    DataViewm(fn.new_page(filename), data=d, command=[[plt]])
    # display first page correctly:
    fn.lift_tab(filename)
    if ifile < nfiles - 1 :
        fn.wait("continue")
    else :
        fn.wait()
