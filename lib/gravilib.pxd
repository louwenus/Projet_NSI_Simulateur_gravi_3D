#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each
#  new/modif of public class in gravilib.cpp

cdef extern from "gravilib.cpp":
    pass

#Declare the class with cdef
cdef extern from "gravilb.h":
    cdef cppclass Dimension:
        Dimension() except +
        Dimension(string) except +
        string hello_text
        string return_hello_world()
        void print_hello_world()
        void set_hello_world(string)
