
# cp Data.py Data.pyx
# python2.6 setup_data.py build_ext --inplace 

import user
from distutils.core import setup 
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("Data", ["Data.pyx"])]

setup(
  name = "Data module",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
