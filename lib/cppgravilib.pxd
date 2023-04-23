#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#  Note: Il faut penser à éditer gravilib.h,gravilib.h & gravilb.pyx 
#  avec chaque modif des classes publiques de gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

from cython import operator, typedef
from cpython cimport PyObject
from libcpp.atomic cimport atomic
from libcpp.list cimport list as clist
ctypedef PyObject* PyObjPtr


cdef extern from "typedef.hpp":
    ctypedef int li
    ctypedef int lli
    ctypedef int uli
    ctypedef int ulli
    bint is_128_bit
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
        SimpleSphere(PyObject* parent,lli x,lli y,lli z,double masse,lli rayon,li vx,li vy,li vz) except +
        llco pos
        uli rayon
        double masse
        atlco speed
        void set_speed(li x,li y,li z)
        void set_masse(double masse)
        void set_ticktime(const float ticktime)
ctypedef DummySphere* DummySpherePtr        

cdef extern from "dimensions/dimension.hpp":
    cdef cppclass BaseDimension :
        BaseDimension() except +
        void add_sphere(DummySphere*)
        void gravite_all()
        void move_all()
        clist[PyObjPtr] detect_collisions()
        const clist[DummySpherePtr] get_sph_list() const