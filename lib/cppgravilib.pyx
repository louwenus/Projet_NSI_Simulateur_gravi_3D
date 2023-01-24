#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

#  Basicaly a wrapper for the dimension class
#  Note: Remenber to edit gravilib.h,gravilib.h & gravilb.pyx with each 
#  new/modif of public class in gravilib.cpp

# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8
# cython: language_level=3

#from libcpp.string cimport string
cimport cppgravilib
import cython

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
        self.c_base_dim.add_sphere(instance.c_dummy_sphere)
    #@property  #! pas pour les trucs privés
    #def hello_text(self) -> str:
    #    return self.c_dim.hello_text
    #@hello_text.setter
    #def hello_text(self, str text) -> None:
    #    self.c_dim.hello_text=text

cdef class CyDummySphere:
    cdef cppgravilib.DummySphere *c_dummy_sphere #C++ instance
    def __cinit__(self,*a,**kw):
        if type(self) is CyDummySphere:
            self.c_dummy_sphere = NULL
    #def __dealloc__(self):
    #    if type(self) is CyDummySphere:
    #        pass
    def debug(self) -> None:
        print("this is a dummy sphere")

cdef class CySimpleSphere(CyDummySphere):
    cdef cppgravilib.SimpleSphere *c_simple_sphere #C++ instance
    def __cinit__(self,int x,int y,int z,int masse,int rayon,int vx,int vy,int vz,int dur):
        if type(self) is CySimpleSphere:
            self.c_simple_sphere = self.c_dummy_sphere = new cppgravilib.SimpleSphere(x,y,z,masse,rayon,vx,vy,vz,dur)
    def __dealloc__(self):
        del self.c_simple_sphere