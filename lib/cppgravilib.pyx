#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#  Basicaly a wrapper for the dimension class
#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each 
#  new/modif of public class in gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

#from libcpp.string cimport string
from os import lchown
from sys import stdout
cimport cppgravilib
from cython.operator import postincrement,dereference
from cpython cimport Py_DECREF, Py_INCREF, PyObject
from libcpp.list cimport list as clist
from typing import Generator, Tuple

ctypedef PyObject* PyObjPtr
ctypedef cppgravilib.DummySphere* DummyPtr
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
    
    def gravite_all(self,float temps) -> None:
        self.c_base_dim.gravite_all(temps)
    def move_all(self,float temps) -> None:
        self.c_base_dim.move_all(temps)
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
        cdef  clist[DummyPtr].iterator iterator = liste.begin()
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
    
    def get_coord(self) -> Tuple[int,int,int]:
        """retourn la position et le rayon au format (x,y,z)
        
        Args:
            self
        
        Returns:
            x (int): composante x de la position
            y (int): composante y de la position
            z (int): composante z de la position
        """
        return 0,0,0
    def get_rayon(self) -> int:
        """retourne le rayon de la sphère"""
        return 0

cdef class CySimpleSphere(CyDummySphere):
    cdef cppgravilib.SimpleSphere *c_simple_sphere
    def init_c_container(self,int x,int y,int z,int masse,int rayon,int vx,int vy,int vz):
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass (aka, need to be called by python derivative)"""
        self.c_simple_sphere = self.c_sphere = new cppgravilib.SimpleSphere(<PyObject*>self,x,y,z,masse,rayon,vx,vy,vz)
    
    def get_coord(self) -> Tuple[int,int,int]:
        return self.c_simple_sphere.pos.x, self.c_simple_sphere.pos.y, self.c_simple_sphere.pos.z
    def set_coord(self,coord:Tuple[int,int,int]) -> None:
        self.c_simple_sphere.pos=coord
    def get_rayon(self) -> int:
        return self.c_simple_sphere.rayon
    def set_rayon(self,rayon:int) -> None:
        self.c_simple_sphere.rayon=rayon
    def get_speed(self) -> Tuple[int,int,int]:
        speed = <cppgravilib.lco>self.c_simple_sphere.speed
        return speed.x,speed.y,speed.z
    def set_speed(self,speed:Tuple[int,int,int]) -> None:
        self.c_simple_sphere.set_speed(speed[0],speed[1],speed[2])
