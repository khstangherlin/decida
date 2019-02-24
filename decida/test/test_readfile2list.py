#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.readfile2list import readfile2list

test_dir = decida.test.test_dir()
for line in readfile2list(test_dir + "data/TextWindow.txt") :
    print(line)
