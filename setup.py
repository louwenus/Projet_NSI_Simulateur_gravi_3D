from setuptools import setup
from Cython.Build import cythonize

setup(
    name='gravilib',
    ext_modules=cythonize("lib/pygravilib.pyx"),
    zip_safe=False,
)
