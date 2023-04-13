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
ctypedef long int li
ctypedef long long int lli
ctypedef unsigned long int uli
ctypedef unsigned long long int ulli

cdef extern from "typedef.hpp":
    struct llco:
        lli x
        lli y
        lli z
    struct lco:
        li x
        li y
        li z
    struct atlco:
        atomic[li] x
        atomic[li] y
        atomic[li] z
        atlco(lco)

cdef extern from "spheres/sphere.hpp":
    cdef cppclass DummySphere:
        DummySphere(PyObject* parent) except +
        PyObject* pyparent
    cdef cppclass SimpleSphere(DummySphere):
        SimpleSphere(PyObject* parent,lli x,lli y,lli z,ulli masse,uli rayon,li vx,li vy,li vz) except +
        llco pos
        uli rayon
        ulli masse
        atlco speed
        void set_speed(li x,li y,li z)
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