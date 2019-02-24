
# cp XYplotx.py XYplotx.pyx
# python2.6 setup_xyplotx.py build_ext --inplace 

import user
from distutils.core import setup 
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("XYplotx", ["XYplotx.pyx"])]

setup(
  name = "XYplotx app",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
