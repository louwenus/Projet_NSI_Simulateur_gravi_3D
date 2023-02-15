import sys
from collections.abc import Iterable

try:
    import cython
except ModuleNotFoundError:
    print("le module cython devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")
    exit(1)

try:
    from . import cppgravilib
except ModuleNotFoundError as e:
    print("cppravilib doit etre compilé pour que ce programme fonctionne, lisez README.md pour plus de détails",file=sys.stderr)
    raise(e)


class PyBaseSphere():
    def __init__(self,cy_sphere_type:cppgravilib.CyDummySphere,args:Iterable) -> None:
        """crée une PyBaseSphere sur la base d'une cy_sphere passé en argument

        Args:
            cy_sphere_type (cppgravilib.CyDummySphere): Le type de cy_sphere sur lequel baser la PyBaseSphere
            args (Iterable): arguments pour la construction de la cy_sphere
        """
        self.cy_sphere=cy_sphere_type(self,*args)
    def render(self):
        x,y,z,rayon = self.cy_sphere.get_coord()

def collide(sph1:PyBaseSphere,sph2:PyBaseSphere,dim:cppgravilib.CyBaseDimension):
    print("ttest")
    return "mwhahaha"