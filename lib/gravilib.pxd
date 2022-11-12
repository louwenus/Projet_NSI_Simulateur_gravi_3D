#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each
#  new/modif of public class in gravilib.cpp

from libcpp.string cimport string

cdef extern from "gravilib.cpp":
    pass

#Declare the class with cdef
cdef extern from "gravilib.h":
    cdef cppclass Dimension:
        string hello_text;
        Dimension() except +;
        void print_hello_world();