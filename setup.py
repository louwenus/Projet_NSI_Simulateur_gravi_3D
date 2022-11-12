from setuptools import setup
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.language_level=3

setup(
    name='graviproject',
    version="0.0.1"
    liscence="GPLv3"
    url="https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D"
    ext_modules=cythonize("lib/pygravilib.pyx"),
    zip_safe=False,
)
