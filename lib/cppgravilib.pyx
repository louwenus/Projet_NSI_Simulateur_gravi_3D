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

cdef class PyBaseDimension:
    cdef BaseDimension *c_base_dim  # Hold a C++ instance, and we forfward everything
    
    def __cinit__(self,*a,**kw):                       #cinit & dealoc pour heritage corect
        if type(self) is PyBaseDimension:
            self.c_base_dim = new BaseDimension()
    def __dealloc__(self):
        if type(self) is PyBaseDimension:
            del self.c_base_dim
    def debug(self) -> None:
        self.c_base_dim.debug()
    
    def print_hello_world(self) -> None:
        self.c_base_dim.print_hello_world()
    def gravite_all(self,float temps) -> None:
        self.c_base_dim.gravite_all(temps)
    def move_all(self,float temps) -> None:
        self.c_base_dim.move_all(temps)
    def add_sphere(self,PyDummySphere instance) -> None:
        self.c_base_dim.add_sphere(instance.c_dummy_sphere)
    def add_simple(self,PySimpleSphere instance) -> None:
        self.c_base_dim.add_sphere(instance.c_simple_sphere)
    #@property  #! pas pour les trucs privés
    #def hello_text(self) -> str:
    #    return self.c_dim.hello_text
    #@hello_text.setter
    #def hello_text(self, str text) -> None:
    #    self.c_dim.hello_text=text

cdef class PyDummySphere:
    cdef DummySphere *c_dummy_sphere #C++ instance
    def __cinit__(self,*a,**kw):
        if type(self) is PyDummySphere:
            self.c_dummy_sphere = new DummySphere()
    def __dealloc__(self):
        if type(self) is PyDummySphere:
            del self.c_dummy_sphere
    def debug(self):
        self.c_dummy_sphere.debug()
cdef class PySimpleSphere(PyDummySphere):
    cdef SimpleSphere *c_simple_sphere #C++ instance
    def __cinit__(self,int x,int y,int z,int masse,int rayon,int vx,int vy,int vz):
        if type(self) is PySimpleSphere:
            self.c_simple_sphere = self.c_dummy_sphere = new SimpleSphere(x,y,z,masse,rayon,vx,vy,vz)
    def __dealloc__(self):
        del self.c_simple_sphere