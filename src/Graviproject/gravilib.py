import sys
from collections.abc import Iterable

try:
    import cython
except ModuleNotFoundError:
    print("le module cython devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")
    exit(1)

try:
    from . import cppgravilib
except ModuleNotFoundError:
    print("cppravilib doit etre compilé pour que ce programme fonctionne, lisez README.md pour plus de détails",file=sys.stderr)
    raise(ModuleNotFoundError)


universe: cppgravilib.CyBaseDimension
class PyBaseSphere():
    def __init__(self,cy_sphere_type:cppgravilib.CyDummySphere,args:Iterable) -> None:
        self.cy_sphere=cy_sphere_type(self,*args)
    def render():
        pass #todo ...
