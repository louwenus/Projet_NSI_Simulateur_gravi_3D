from setuptools import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.language_level=3

setup(
    name='gravilib',
    ext_modules=cythonize("lib/pygravilib.pyx"),
    zip_safe=False,
)
