from setuptools import setup
from Cython.Build import cythonize

setup(
    name='gravilib',
    ext_modules=cythonize("lib/gravilib.pyx"),
    zip_safe=False,
)
