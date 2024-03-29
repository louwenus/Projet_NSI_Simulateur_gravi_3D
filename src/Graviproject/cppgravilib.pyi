#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding = utf8
from typing import Generator

is_128_bit:bool
def set_ticktime(ticktime:float)-> None: ...

class CySimpleSphere():
    def init_c_container(self,x:int,y:int,z:int,masse:int,rayon:int,vx:float,vy:float,vz:float) -> None:
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass
        (aka, need to be called by python derivative)"""
    def get_coord(self) -> tuple[int,int,int]: ...
    def set_coord(self,coord:tuple[int,int,int]) -> None: ...
    def get_speed(self) -> tuple[int,int,int]: ...
    def set_speed(self,speed:tuple[int,int,int]) -> None: ...
    def get_energie(self) -> tuple[float,float,float]: ...
    def set_energie(self,energie:tuple[float,float,float]) -> None:...
    def get_rayon(self) -> int: ...
    def set_rayon(self,rayon:int) -> None: ...
    def get_render_items(self) -> list: return []
    def get_masse(self) -> int: ...
    def set_masse(self,masse:float) -> None: ...

class CyBaseDimension():
    def init_c_container(self) -> None:
        """For this class to work, this function HAVE TO BE CALLED, however, it can be skipped if c_base_dim is set by subclass
        (aka, should be called once by final python derived class)"""
    def gravite_all(self) -> None: ...
    def move_all(self) -> None: ...
    def add_sphere(self,instance:CySimpleSphere) -> None: ...
    def collisions(self) -> Generator[tuple[CySimpleSphere,CySimpleSphere]]: ...
    def get_spheres(self) -> Generator[CySimpleSphere]: ...