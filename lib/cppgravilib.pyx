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
from cpython cimport PyObject
from libcpp.list cimport list as clist
from typing import Callable, Tuple

ctypedef PyObject* PyObjPtr
cdef class CyBaseDimension:
    cdef cppgravilib.BaseDimension *c_base_dim  # Hold a C++ instance, and we forfward everything

    def __cinit__(self,*a,**kw):                       #cinit & dealoc pour heritage corect
        if type(self) is CyBaseDimension:
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
    
    def collisions(self,fonction:Callable) -> list:
        """Détecte les collisions dans une dimension, puis appelle la fonction passée en argument pour chacune:
      fonction(sphere1,sphere2,dimension), les retours de cette fonction sont ajoutés dans une liste, qui est renvoyée.
        
        Args:
            self (CyBaseDimension): La CyBaseDimension (ou compatible) sur laquelle on detecte les collisions
            fonction (function): La fonction de collision, prend 3 arguments, 2 PyBaseSphere (ou compatible) et une CyBaseDimension(ou compatible)
        
        Returns:
            retours (list): La concatenation sous forme de liste des résultats de la fonction sur chaque collisions
        """
        cdef clist[PyObjPtr] liste 
        liste = self.c_base_dim.detect_collisions()
        liste2 : list = []
        cdef  clist[PyObjPtr].iterator iterator = liste.begin()
        cdef object obje,obje2
        while iterator!=liste.end():
        #    liste2.append(<object>dereference(preincrement(iterator)))
            obje = <object>dereference(postincrement(iterator))
            obje2 = <object>dereference(postincrement(iterator))
            liste2.append(fonction(obje,obje2,self))
        return liste2

    #@property  #! pas pour les trucs privés
    #def hello_text(self) -> str:
    #    return self.c_dim.hello_text
    #@hello_text.setter
    #def hello_text(self, str text) -> None:
    #    self.c_dim.hello_text=text

cdef class CyDummySphere:
    cdef cppgravilib.DummySphere *c_sphere #C++ instance
    def __cinit__(self,*a,**kw):
        if type(self) is CyDummySphere:
            self.c_sphere = NULL
    def __dealloc__(self):
        del self.c_sphere
    def debug(self) -> None:
        """print out debuging info on stdout"""
        print("this is a dummy sphere")
    
    def get_coord(self):
        """retourn la position et le rayon au format (x,y,z,rayon)
        
        Args:
            self
        
        Returns:
            x (int): composante x de la position
            y (int): composante y de la position
            z (int): composante z de la position
            rayon (int): rayon"""
        return 0,0,0,0

cdef class CySimpleSphere(CyDummySphere):
    cdef cppgravilib.SimpleSphere *c_simple_sphere #C++ instance
    def __cinit__(self,object parent,int x,int y,int z,int masse,int rayon,int vx,int vy,int vz,*a,**kw):
        if type(self) is CySimpleSphere:
            self.c_sphere = new cppgravilib.SimpleSphere(<PyObject*>parent,x,y,z,masse,rayon,vx,vy,vz)
    
    def get_coord(self) -> Tuple[int,int,int,int]:
        return self.c_simple_sphere.pos.x, self.c_simple_sphere.pos.y, self.c_simple_sphere.pos.z, self.c_simple_sphere.rayon
    
