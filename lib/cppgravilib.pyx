#  Basicaly a wrapper for the dimension class
#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each 
#  new/modif of public class in gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3


#from libcpp.string cimport string
from cppgravilib cimport Dimension
import cython

cdef class PyDimension:
    cdef Dimension c_dim  # Hold a C++ instance, and we forfward everything
    def __init__(self):
        self.c_dim = Dimension()
    def print_hello_world(self) -> None:
        self.c_dim.print_hello_world()
    @property  #! pas pour les trucs privés
    def hello_text(self) -> str:
        return self.c_dim.hello_text
    @hello_text.setter
    def hello_text(self, str text) -> None:
        self.c_dim.hello_text=text