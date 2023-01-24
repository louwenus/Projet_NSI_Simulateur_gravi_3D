#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
#  avec chaque modif des classes publiques de gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

from libcpp.string cimport string

cdef extern from "spheres/sphere.hpp":
    cdef cppclass DummySphere:
        pass
    cdef cppclass SimpleSphere(DummySphere):
        SimpleSphere(int x,int y,int z,int masse,int rayon,int vx,int vy,int vz,int dur) except +

cdef extern from "dimensions/dimension.hpp":
    cdef cppclass BaseDimension :
        BaseDimension() except +
        void add_sphere(DummySphere*)
        void gravite_all(float temps)
        void move_all(float temps)
        void debug()