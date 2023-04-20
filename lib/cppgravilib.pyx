#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#  Basicaly a wrapper for the dimension class
#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each 
#  new/modif of public class in gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

#from libcpp.string cimport string
cimport cppgravilib
from cython.operator import postincrement,dereference
from cpython cimport Py_DECREF, Py_INCREF, PyObject
from libcpp.list cimport list as clist
from typing import Generator, Tuple

ctypedef PyObject* PyObjPtr
ctypedef cppgravilib.DummySphere* DummyPtr
ctypedef long int li
ctypedef long long int lli
ctypedef unsigned long int uli
ctypedef unsigned long long int ulli

cdef class CyBaseDimension:
    cdef cppgravilib.BaseDimension *c_base_dim  # Hold a C++ instance, and we forfward everything

    def init_c_container(self):                             
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass
        (aka, should be called once by final python derived class)"""
        self.c_base_dim = new cppgravilib.BaseDimension()

    def __dealloc__(self):
        if type(self) is CyBaseDimension:
            del self.c_base_dim
    def debug(self) -> None:
        self.c_base_dim.debug()
    
    def gravite_all(self) -> None:
        self.c_base_dim.gravite_all()
    def move_all(self) -> None:
        self.c_base_dim.move_all()
    def add_sphere(self,CyDummySphere instance) -> None:
        self.c_base_dim.add_sphere(instance.c_sphere)
    
    def collisions(self) -> Generator:
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
    def get_spheres(self) -> Generator:
        cdef clist[DummyPtr] liste = self.c_base_dim.get_sph_list()
        cdef clist[DummyPtr].iterator iterator = liste.begin()
        cdef DummyPtr obj
        while iterator!=liste.end():
            obj = dereference(postincrement(iterator))
            yield <object>(obj.pyparent)
    #@property  #! pas pour les trucs privés
    #def hello_text(self) -> str:
    #    return self.c_dim.hello_text
    #@hello_text.setter
    #def hello_text(self, str text) -> None:
    #    self.c_dim.hello_text=text

cdef class CyDummySphere:
    cdef cppgravilib.DummySphere *c_sphere
    def init_c_container(self):                             
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass (aka, need to be called by python derivative)"""
        self.c_sphere = NULL
    def __dealloc__(self):
        del self.c_sphere
    def debug(self) -> None:
        """print out debuging info on stdout"""
        print("this is a dummy sphere")
    
    def get_coord(self) -> Tuple[lli,lli,lli]:
        return 0,0,0
    def set_coord(self,coord:Tuple[lli,lli,lli]) -> None:
        pass
    def get_rayon(self) -> uli:
        return 0
    def set_rayon(self,rayon:uli) -> None:
        pass
    def get_speed(self) -> Tuple[li,li,li]:
        return 0,0,0
    def set_speed(self,speed:Tuple[li,li,li]) -> None:
        pass
    def set_ticktime(self,ticktime:float) -> None:
        pass

cdef class CySimpleSphere(CyDummySphere):
    cdef cppgravilib.SimpleSphere *c_simple_sphere
    def init_c_container(self,lli x,lli y,lli z,ulli masse,uli rayon,li vx,li vy,li vz):
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass (aka, need to be called by python derivative)"""
        self.c_simple_sphere = self.c_sphere = new cppgravilib.SimpleSphere(<PyObject*>self,x,y,z,masse,rayon,vx,vy,vz)
    
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
    def get_speed(self) -> Tuple[li,li,li]:
        speed = <cppgravilib.lco>self.c_simple_sphere.speed
        return speed.x,speed.y,speed.z
    def set_speed(self,speed:Tuple[li,li,li]) -> None:
        self.c_simple_sphere.set_speed(speed[0],speed[1],speed[2])
    def get_masse(self) -> ulli:
        return self.c_simple_sphere.masse
    def set_masse(self,masse:ulli) -> None:
        self.c_simple_sphere.set_masse(masse)
    def set_ticktime(self,ticktime:float) -> None:
        self.c_simple_sphere.set_ticktime(<const float>ticktime)
