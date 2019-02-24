#!/usr/bin/env python
from __future__ import print_function
import re
import glob
import decida
import decida.test
from decida.Data import Data

test_dir = decida.test.test_dir()
files = glob.glob(test_dir + "/data/*/*/*") 
files.extend(glob.glob(test_dir + "/data/*.csv"))
files.extend(glob.glob(test_dir + "/data/*.report"))
files.extend(glob.glob(test_dir + "/data/*.col"))
for file in files :
    datafile_format = Data.datafile_format(file)
    file_tail = re.sub("^" + test_dir + "/data/", "", file)
    print("%-25s: %s" % (file_tail, datafile_format))
