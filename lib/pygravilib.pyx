# distutils: language = c++

#  Basicaly a wrapper for the dimension class
#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each 
#  new/modif of public class in gravilib.cpp

from gravilib cimport Dimension

cdef class PyDimension:
    cdef Dimension c_dim  # Hold a C++ instance, and we forfward everything
    
    def __init__(self, str text):
        self.c_dim = Dimension(text)
    def print_hello_world(self):
        self.c_dim.print_hello_world
    def return_hello_world(self):
        return self.c_dim.return_hello_world()
    def set_hello_world(self, str text):
        self.c_dim.set_hello_world(text)
    #@property  #! pas pour les trucs privés
    #def hello_text(self):
    #    return self.c_dim.hello_text
    #@hello_text.setter
    #def hello_text(self, str text):
    #    self.c_dim.hello_text=text
