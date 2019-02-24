################################################################################
# NAME     : .pythonrc.py
# PURPOSE  : python resource file
# AUTHOR   : Richard Booth
# DATE     : Sun Nov 10 19:46:20 2013
# -----------------------------------------------------------------------------
# NOTES    : 
#     * provide local user python directory
#     * in scripts, import user
#     * sys.platform in "cygwin", "linux", "darwin", "win32"
########################################################################
import sys, os, os.path

pylib = os.path.abspath("~/.DeCiDa/lib")
if (not (pylib in sys.path)) : sys.path.insert(0, pylib)

def module_list () :
    modules =  sys.modules.keys()
    modules.sort()
    for module in modules :
         print module + " -> " + str(sys.modules[module])
