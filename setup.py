from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
from Cython.Compiler import Options
import os

Options.language_level = 3
copt: dict[str, list[str]] = {# 'unix': ['-std=gnu++20', '-g', '-Og', '-pthread', '-ffast-math'],
                              'unix': ['-std=gnu++20','-O3','-pthread','-ffast-math']  ,
                              'mingw32': ['-std=gnu++20', '-O3', '-pthread', '-ffast-math'],
                              'mingw64': ['-std=gnu++20', '-O3', '-pthread', '-ffast-math'],
                              'msvc': ['/std:c++20', '/cgthreads8', '/O2', '/GL'],
                              # 'cygiwin' : []
                              }
sourcesfiles: list[str] = []
for folder, folders, files in os.walk("lib"):
    for file in files:
        if file.split(".")[-1] in ("pyx", "cpp"):  # ,"pxd"
            if file not in ("cppgravilib.cpp"):
                sourcesfiles.append(folder + "/" + file)

cppgravilib: list[Extension] = [Extension("Graviproject.cppgravilib", sources=sourcesfiles, include_dirs=[
                                          './lib/', './lib/dimensions', './lib/spheres'], language="c++")]


class build_ext_subclass(build_ext):
    def build_extensions(self) -> None:
        compiler = self.compiler.compiler_type
        print("using compiler:", compiler)
        if compiler in copt.keys():
            print("which is a known compiler, applying extra args:",
                  copt[compiler])
            for e in self.extensions:
                e.extra_compile_args = copt[compiler]
            build_ext.build_extensions(self)
        else:
            print("ERROR:", compiler, "is NOT a known compiler, you should add relevant compiler specific args to copt and/or report to devs")
            exit(1)


setup(
    ext_modules=cythonize(cppgravilib),
    cmdclass={'build_ext': build_ext_subclass}
)
