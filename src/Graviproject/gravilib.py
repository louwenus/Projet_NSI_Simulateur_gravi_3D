import sys
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


universe: cppgravilib.PyBaseDimension
class PySimpleSphere(cppgravilib.CySimpleSphere):
    def __init__(self,x:int,y:int,z:int,masse:int,rayon:int,vx:int,vy:int,vz:int,dur:int) -> None:
        super().__init__(x,y,z,masse,rayon,vx,vy,vz,dur)
