from setuptools import setup, Extension
#from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.language_level=3

#copt =  {'gcc': ['-std=c++20']  ,
#     'clang' : ['-std=c++20']   ,
#     'msvc'  : []  }

cppgravilib = [Extension("cppgravilib",sources=["lib/cppgravilib.pyx"],include_dirs=['./lib/', './lib/dimensions','./lib/spheres'],language="c++",extra_compile_args=['-std=c++20','-g','-Og','-pthread'])]

 #class build_ext_subclass( build_ext ):
 #   def build_extensions(self):
 #       c = self.compiler.compiler_type
 #       if copt.has_key(c):
 #          for e in self.extensions:
 #              e.extra_compile_args = copt[ c ]
 #       #if lopt.has_key(c):
 #       #    for e in self.extensions:
 #       #        e.extra_link_args = lopt[ c ]
 #       build_ext.build_extensions(self)

setup(
    ext_modules=cythonize(cppgravilib),
#    cmdclass = {'build_ext': build_ext_subclass}
)