#  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
#  avec chaque modif des classes publiques de gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

from libcpp.string cimport string

cdef extern from "gravilib.cpp":
    pass

#Declare the class with cdef
cdef extern from "gravilib.h":
    cdef cppclass Dimension :
        Dimension() except +
        string hello_text
        void print_hello_world()