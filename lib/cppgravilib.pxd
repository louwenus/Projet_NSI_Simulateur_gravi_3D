#  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
#  avec chaque modif des classes publiques de gravilib.cpp

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

from libcpp.string cimport string

cdef extern from "main.hpp":
    pass

#Declare the class with cdef
cdef extern from "dimensions/dimension.hpp":
    cdef cppclass BaseDimension :
        BaseDimension() except +
        string hello_text
        void print_hello_world()