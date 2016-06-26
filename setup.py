import setuptools
from distutils.core import setup
from distutils.extension import Extension
#from Cython.Distutils import build_ext
from Cython.Build import cythonize

setuptools.setup(
    name='PyBaccarat',
    version='0.1dev',
    packages=['baccarat',],
    long_description=open('README.txt').read(),
    #cmdclass = {'build_ext': build_ext},
    #ext_modules = [Extension("baccarat1_so", ["baccarat/baccarat1.pyx"]),
    #               Extension("baccarat2_so", ["baccarat/baccarat2.pyx"]),
    #               Extension("baccarat3_so", ["baccarat/baccarat3.pyx"]),
    #]
    ext_modules = cythonize("baccarat/*.pyx")
    #install_requires = ['Cython', 'line-profiler', 'memory-profiler']
)
