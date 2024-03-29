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
    float ticktime
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
    struct dbco:
        double x
        double y
        double z

cdef extern from "spheres/sphere.hpp":
    cdef cppclass SimpleSphere:
        SimpleSphere(PyObject* parent,lli x,lli y,lli z,double masse,lli rayon,float vx,float vy,float vz) except +
        PyObject* pyparent
        llco pos
        uli rayon
        double masse
        void set_speed(float x,float y,float z)
        dbco get_speed()
        void set_energie(double x,double y,double z)
        dbco get_energie()
        void set_masse(double masse)
ctypedef SimpleSphere* SpherePtr        

cdef extern from "dimensions/dimension.hpp":
    cdef cppclass BaseDimension :
        BaseDimension() except +
        void add_sphere(SimpleSphere*)
        void gravite_all()
        void move_all()
        clist[PyObjPtr] detect_collisions()
        const clist[SpherePtr] get_sph_list() const