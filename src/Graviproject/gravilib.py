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
    print("cppravilib doit etre compilé pour que ce programme fonctionne, lisez README.md pour plus de détails", file=sys.stderr)
    raise (e)
from .affichage3D import SphereItem


class PyBaseSphere(cppgravilib.CySimpleSphere):
    def __init__(self, x: int, y: int, z: int, masse: int, rayon: int, vx: int, vy: int, vz: int, d: int) -> None:
        """crée une PyBaseSphere sur la base d'une cySimpleSphere

        Args:
            x,y,z (int): position de départ de la sphere
            masse,rayon (int): self-explicit
            vx,vy,vz (int): vitesse de départ de la sphère
        """
        self.init_c_container(x, y, z, masse, rayon, vx, vy, vz)
        self.render_item: SphereItem = SphereItem(
            self.get_rayon(), self.get_coord)

    def get_render_items(self) -> list[SphereItem]:
        return [self.render_item]
        # now, use position and size, plus information embded in the python object (like color) to render the sphere

    def rebond(self):
        vx,vy,vz=self.get_speed()
        vx = vx*(-1)
        vy = vy*(-1)
        vz = vz*(-1)
        self.set_speed((vx, vy, vz))
    
def absorbtion (sphere1, sphere2):
    for render in sphere1.get_render_items():
        vol_1 = render.volume_sphere()
    for render in sphere2.get_render_items():
        vol_2 = render.volume_sphere()
    if vol_1 > vol_2:
        for render in sphere1.get_render_items():
            render.grossir(vol_2/3)
        for render in sphere2.get_render_items():
            render.disparaitre()
    else:
        for render in sphere2.get_render_items():
            render.grossir(vol_1/3)
        for render in sphere1.get_render_items():
            render.disparaitre()


class PyBaseDimension(cppgravilib.CyBaseDimension):
    def __init__(self) -> None:
        self.init_c_container()

    def gerer_colision(self) -> None:
        for sphere, sphere2 in self.collisions():
            sphere.rebond()
            sphere2.rebond()
            # absorbtion(sphere, sphere2)
            for render in sphere.get_render_items() + sphere2.get_render_items():
                render.change_couleur()
            self.add_sphere(sphere)
            self.add_sphere(sphere2)