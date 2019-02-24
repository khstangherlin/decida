#!/usr/bin/env python
from __future__ import print_function
import decida

def lev1():
    var1 = "test"
    var2 = 1
    var3 = 2.3e-10
    var4 = ["1", "2", "3"]
    var5 = [1, 2, 3]
    var6 = [1.2, 2.3e10, 3]

    ctrl = decida.interpolate("""
      var1 = $var1
      var2 = $var2
      var3 = $var3
      var4 = $var4
      var5 = $var5
      var6 = $var6
      var7 = $var7
      var8 = $var8

      var1 = ${var1}_xxx
      var2 = ${var2}_xxx
      var3 = ${var3}_xxx
      var4 = ${var4}_xxx
      var5 = ${var5}_xxx
      var6 = ${var6}_xxx
      var7 = ${var7}_xxx
      var8 = ${var8}_xxx
    """)
    print("lev1 ctrl = ", ctrl)

def lev2():
    ctrl = decida.interpolate("""
      var0 = $var0
    """)
    print("lev2 ctrl = ", ctrl)

var0 = "___"
var7 = "XXX"
var8 = "YYY"
lev1()
lev2()
