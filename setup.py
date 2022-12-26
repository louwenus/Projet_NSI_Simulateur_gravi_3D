from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.language_level=3

copt =  {'unix': ['-std=c++20','-g','-Og','-pthread','-ffast-math']  ,
        #'mingw32' : ['-std=c++20']   ,
        #'msvc'  : []  , 
        #'cygiwin' : []
}

cppgravilib = [Extension("Graviproject.cppgravilib",sources=["lib/dimensions/dimension.cpp","lib/spheres/simple_sphere.cpp","lib/spheres/dummy_sphere.cpp","lib/cppgravilib.pyx","lib/cppgravilib.pxd"],include_dirs=['./lib/', './lib/dimensions','./lib/spheres'],language="c++")]

class build_ext_subclass( build_ext ):
    def build_extensions(self):
        c = self.compiler.compiler_type
        print("using compiler:",c)
        if c in copt.keys():
            print("wich is a knwon compiler, aplying extra args:",copt[c])
            for e in self.extensions:
                e.extra_compile_args = copt[ c ]
            build_ext.build_extensions(self)
        else:
            print("ERROR:",c,"is NOT a known compiler, you should add relevant compiler specific args to copt and/or report to devs")
            exit(1)

setup(
    ext_modules=cythonize(cppgravilib),
    cmdclass = {'build_ext': build_ext_subclass}
)