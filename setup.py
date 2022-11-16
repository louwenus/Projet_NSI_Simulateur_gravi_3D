from setuptools import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.language_level=3

setup(
    ext_modules=cythonize("lib/pygravilib.pyx"),
)