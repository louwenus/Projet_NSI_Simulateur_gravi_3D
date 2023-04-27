#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#  Basicaly a wrapper for the dimension class
#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each 
#  new/modif of public class in gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

cimport cppgravilib
from cython.operator import postincrement,dereference
from cpython cimport Py_DECREF, Py_INCREF, PyObject
from libcpp.list cimport list as clist
from typing import Generator, Tuple

cdef extern from "typedef.hpp":
    ctypedef int li
    ctypedef int lli
    ctypedef int uli
    ctypedef int ulli
    struct dbco:
        double x
        double y
        double z


ctypedef PyObject* PyObjPtr
ctypedef cppgravilib.SimpleSphere* SpherePtr

is_128_bit:bool = cppgravilib.is_128_bit
def set_ticktime(float ticktime):
    if ticktime==0:
        raise ZeroDivisionError
    cppgravilib.ticktime=ticktime


cdef class CyBaseDimension:
    cdef cppgravilib.BaseDimension *c_base_dim  # Hold a C++ instance, and we forfward everything

    def init_c_container(self):                             
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass
        (aka, should be called once by final python derived class)"""
        self.c_base_dim = new cppgravilib.BaseDimension()

    def __dealloc__(self):
        if type(self) is CyBaseDimension:
            del self.c_base_dim

    def gravite_all(self) -> None:
        self.c_base_dim.gravite_all()
    def move_all(self) -> None:
        self.c_base_dim.move_all()
    def add_sphere(self,CySimpleSphere instance) -> None:
        self.c_base_dim.add_sphere(instance.c_simple_sphere)
    
    def collisions(self) -> Generator[Tuple[CySimpleSphere,CySimpleSphere]]:
        """Détecte les collisions dans une dimension, puis retourne un iterator sur les sphères.
        
        Args:
            self (CyBaseDimension): La CyBaseDimension (ou compatible) sur laquelle on detecte les collisions
        
        Returns:
            retours (iterator): Iterateur sur les paires de sphères
        """
        cdef clist[PyObjPtr] liste 
        liste = self.c_base_dim.detect_collisions()
        cdef  clist[PyObjPtr].iterator iterator = liste.begin()
        cdef object obje,obje2
        while iterator!=liste.end():
            obje = <object>dereference(postincrement(iterator))
            obje2 = <object>dereference(postincrement(iterator))
            yield obje,obje2
    def get_spheres(self) -> Generator[CySimpleSphere]:
        cdef clist[SpherePtr] liste = self.c_base_dim.get_sph_list()
        cdef clist[SpherePtr].iterator iterator = liste.begin()
        cdef SpherePtr obj
        while iterator!=liste.end():
            obj = dereference(postincrement(iterator))
            yield <object>(obj.pyparent)



cdef class CySimpleSphere():
    cdef cppgravilib.SimpleSphere *c_simple_sphere
    def init_c_container(self,lli x,lli y,lli z,double masse,lli rayon,li vx,li vy,li vz):
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass (aka, need to be called by python derivative)"""
        self.c_simple_sphere = new cppgravilib.SimpleSphere(<PyObject*>self,x,y,z,masse,rayon,vx,vy,vz)
    
    def get_coord(self) -> Tuple[lli,lli,lli]:
        return self.c_simple_sphere.pos.x, self.c_simple_sphere.pos.y, self.c_simple_sphere.pos.z
    def set_coord(self,coord:Tuple[lli,lli,lli]) -> None:
        cdef cppgravilib.llco co
        co.x=coord[0];  co.y=coord[1];  co.z=coord[2]
        self.c_simple_sphere.pos=co
    def get_rayon(self) -> uli:
        return self.c_simple_sphere.rayon
    def set_rayon(self,rayon:uli) -> None:
        self.c_simple_sphere.rayon=rayon
    def get_speed(self) -> Tuple[double,double,double]:
        cdef dbco speed = self.c_simple_sphere.get_speed()
        return speed.x,speed.y,speed.z
    def set_speed(self,speed:Tuple[li,li,li]) -> None:
        self.c_simple_sphere.set_speed(speed[0],speed[1],speed[2])
    def get_energie(self) -> Tuple[double,double,double]:
        cdef dbco energie = self.c_simple_sphere.get_energie()
        return energie.x,energie.y,energie.z
    def set_energie(self, energie:Tuple[double,double,double]) -> None:
        self.c_simple_sphere.set_energie(energie[0],energie[1],energie[2])
    def get_masse(self) -> ulli:
        return self.c_simple_sphere.masse
    def set_masse(self,double masse) -> None:
        self.c_simple_sphere.set_masse(masse)
