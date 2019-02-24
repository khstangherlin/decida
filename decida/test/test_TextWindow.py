#!/usr/bin/env python
import decida
import decida.test
from decida.TextWindow import TextWindow

test_dir = decida.test.test_dir()
filename = test_dir + "data/TextWindow.txt"
twin = TextWindow(text_height=30, wait=False)
twin.fileread(filename)
twin["text_width"]  = 90
twin.wait("continue")
twin.clear()
twin.wait()
