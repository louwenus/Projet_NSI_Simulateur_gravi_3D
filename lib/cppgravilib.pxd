#  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
#  avec chaque modif des classes publiques de gravilib.cpp

from libcpp.string cimport string

cdef extern from "gravilib.cpp":
    pass

#Declare the class with cdef
cdef extern from "gravilib.h":
    cdef cppclass Dimension :
        Dimension() except +
        string hello_text
        void print_hello_world()