#!/usr/bin/env python
from __future__ import print_function
import sys
import os.path

def test_dir() :
    for d in sys.path :
        filename = "%s/decida/test/test_dir.py" % (d)
        if os.path.isfile(filename) :
            return(d + "/decida/test/")
    print("can't locate decida test directory")
    exit()
