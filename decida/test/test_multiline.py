#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test
from decida.readfile2list import readfile2list

test_dir = decida.test.test_dir()
lines = readfile2list(test_dir + "data/TextWindow.txt")

for line in lines :
    for uline in decida.multiline(line, 20) :
        print(uline)
