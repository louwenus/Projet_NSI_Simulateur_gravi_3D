#  Basicaly a wrapper for the dimension class
#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each 
#  new/modif of public class in gravilib.cpp

#   Simulateur_gravi_3D : Un simulateur de gravité simple avec rendu 3D
#   Copyright (C) 2022 louwenus, Artefact42, kalyklos, Bjctrhtg, g-aled
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3


#from libcpp.string cimport string
cimport cppgravilib
import cython

cdef class PyBaseDimension:
    cdef BaseDimension *c_base_dim  # Hold a C++ instance, and we forfward everything
    
    def __cinit__(self,*a,**kw):                       #cinit & dealoc pour heritage corect
        if type(self) is PyBaseDimension:
            self.c_base_dim = new BaseDimension()
    def __dealloc__(self):
        if type(self) is PyBaseDimension:
            del self.c_base_dim
    


    def print_hello_world(self) -> None:
        self.c_dim.print_hello_world()
    def gravite_all(self) -> None:
        self.c_dim.gravite_all()
    def move_all(self) -> None:
        self.c_dim.move_all()
    #@property  #! pas pour les trucs privés
    #def hello_text(self) -> str:
    #    return self.c_dim.hello_text
    #@hello_text.setter
    #def hello_text(self, str text) -> None:
    #    self.c_dim.hello_text=text

cdef class PyDummySphere:
    cdef DummySphere *c_dummy_sph #C++ instance
    def __cinit__(self,*a,**kw):
        if type(self) is PyDummySphere:
            self.c_dummy_sph = new DummySphere()
    def __dealloc__(self):
        if type(self) is PyDummySphere:
            del self.c_dummy_sph

cdef class PySimpleSphere:
    cdef SimpleSphere *c_simple_sphere #C++ instance
    def __cinit__(int x,int y,int z,int masse,int rayon,int vx,int vy,int vz):
        
