#!/usr/bin/env python
from __future__ import print_function
import decida
import decida.test


test_dir = decida.test.test_dir()
tests = decida.test.test_list()
skip_tests = ("test_XYplotm_1", "test_Tckt_1")

print("@" * 70)
print(" DeDiDa tests ...")
print("@" * 70)

for test in tests :
    if test in skip_tests :
        print("@" * 70)
        print(" skipping ", test, ":")
        print(" try this test separately")
        print("@" * 70)
        continue
    print(" ... %s ... " % (test))
    if test in ("test_FrameNotebook_1", "test_FrameNotebook_2"):
        print("@" * 70)
        print(" ", test, ":")
        print("  press each \"Continue\" button ...")
        print("  exit test by pressing \"Quit\" when it becomes active ...")
        print("@" * 70)
    elif test in ("test_NGspice_1", "test_NGspice_2", "test_NGspice_3") :
        print("@" * 70)
        print(" ", test, ":")
        print("  press \"Simulate/Plot\" to run simulation ...")
        print("  close window to exit test")
        print("@" * 70)
    test_py = "%s/%s.py" % (test_dir, test)
    response = decida.syscall("/usr/bin/env python " + test_py)
    if response :
        print(response)
