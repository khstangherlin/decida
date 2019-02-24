#!/usr/bin/env python
from __future__ import print_function
import re
import glob
import decida
import decida.test
from decida.Data import Data

test_dir = decida.test.test_dir()
for file in glob.glob(test_dir + "/data/*/*/*") :
    datafile_format = Data.datafile_format(file)
    if datafile_format == "nutmeg":
        file_tail = re.sub("^" + test_dir + "/data/", "", file)
        blocks = Data.nutmeg_blocks(file)
        print(file_tail, ":")
        for block in blocks :
            print("    ", block)
