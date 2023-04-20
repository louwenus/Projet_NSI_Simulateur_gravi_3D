#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding = utf8
from typing import Generator

class CyDummySphere:
    def init_c_container(self):                             
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass 
        aka, need to be called by python derivative)"""
    def debug(self) -> None: ...
    def get_coord(self) -> tuple[int,int,int]: ...
    def set_coord(self,coord:tuple[int,int,int]): ...
    def get_speed(self) -> tuple[int,int,int]: ...
    def set_speed(self,coord:tuple[int,int,int]): ...
    def get_rayon(self) -> int: ...
    def set_rayon(self,rayon:int) -> None: ...
    def set_ticktime(self,ticktime:float) -> None: ...

class CySimpleSphere(CyDummySphere):
    def init_c_container(self,x:int,y:int,z:int,masse:int,rayon:int,vx:int,vy:int,vz:int):
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass
        (aka, need to be called by python derivative)"""
    def get_masse(self) -> int: ...
    def set_masse(self,masse:int) -> None: ...

class CyBaseDimension():
    def init_c_container(self) -> None:
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass
        (aka, should be called once by final python derived class)"""
    def debug(self) -> None: ...
    def gravite_all(self) -> None: ...
    def move_all(self) -> None: ...
    def add_sphere(self,instance:CyDummySphere) -> None: ...
    def collisions(self) -> Generator[tuple[CyDummySphere,CyDummySphere]]: ...
    def get_spheres(self) -> Generator[CyDummySphere]: ...