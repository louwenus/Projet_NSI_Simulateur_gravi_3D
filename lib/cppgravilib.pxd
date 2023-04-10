#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
#  avec chaque modif des classes publiques de gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

from cython import operator
from cpython cimport PyObject
from libcpp.atomic cimport atomic
from libcpp.list cimport list as clist
ctypedef PyObject* PyObjPtr

cdef extern from "typedef.hpp":
    struct llco:
        int x
        int y
        int z
    struct lco:
        int x
        int y
        int z
    struct atlco:
        atomic[int] x
        atomic[int] y
        atomic[int] z
        atlco(lco)

cdef extern from "spheres/sphere.hpp":
    cdef cppclass DummySphere:
        DummySphere(PyObject* parent) except +
        PyObject* pyparent
    cdef cppclass SimpleSphere(DummySphere):
        SimpleSphere(PyObject* parent,int x,int y,int z,int masse,int rayon,int vx,int vy,int vz) except +
        llco pos
        int rayon
        int masse
        atlco speed
        void set_speed(int x,int y,int z)
ctypedef DummySphere* DummySpherePtr        

cdef extern from "dimensions/dimension.hpp":
    cdef cppclass BaseDimension :
        BaseDimension() except +
        void add_sphere(DummySphere*)
        void gravite_all(float temps)
        void move_all(float temps)
        void debug()
        clist[PyObjPtr] detect_collisions()
        clist[DummySpherePtr] get_sph_list()