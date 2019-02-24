#!/usr/bin/env python
import os
import decida.test

def test_list() :
    files = os.listdir(decida.test.test_dir())
    non_tests = ("__init__", "test_list", "test_dir", "test_all")
    test_list = []
    for filename in files :
        tail = os.path.basename(filename)
        root, ext = os.path.splitext(tail)
        if ext == ".py" and not root in non_tests :
            test_list.append(root)
    test_list.sort()
    return test_list
