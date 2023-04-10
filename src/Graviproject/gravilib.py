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
            d (int) : dureté de la balle
        """
        self.durete = d
        self.rayon = rayon
        self.init_c_container(x, y, z, masse, rayon, vx, vy, vz)
        self.render_item: SphereItem = SphereItem(
            self.get_rayon(), self.get_coord)

    def get_render_items(self) -> list[SphereItem]:
        return [self.render_item]

    def rebond(self) -> None:
        """Inverse la trajectoire d'une sphere
        """
        vx,vy,vz=self.get_speed()
        vx = vx*(-1)
        vy = vy*(-1)
        vz = vz*(-1)
        self.set_speed((vx, vy, vz))
    
def absorption (sphere1:PyBaseSphere, sphere2:PyBaseSphere):
    """ Fonction prenant en paramètre 2 sphères, renvoyant l'absorption de la plus petite par la plus grosse.
    Args:
        sphere1, sphere2 : objet de la class PyBaseSphere
    """
    vol_1 = sphere1.get_rayon()
    vol_2 = sphere2.get_rayon()
    if vol_1 > vol_2:
        for render in sphere1.get_render_items():
            render.grossir(vol_2/5)
        for render in sphere2.get_render_items():
            render.disparaitre()
    else:
        for render in sphere2.get_render_items():
            render.grossir(vol_1/5)
        for render in sphere1.get_render_items():
            render.disparaitre()
def trans(m1,v1,m2,v2):
    vf1=(2*m2*v2+v1*(m1-m2))/(m1+m2)
    vf2=(2*m1*v1+v2*(m2-m1))/(m1+m2)
    
    return vf1,vf2    

class PyBaseDimension(cppgravilib.CyBaseDimension):
    def __init__(self) -> None:
        self.init_c_container()

    def gerer_colision(self) -> None:
        """ Fonction s'occupant des collisions, faisant rebondir ou s'absorber 2 objet sphere de la class PyBaseSphere
        """
        ajouter_sphere_1 = True
        ajouter_sphere_2 = True
        for sphere, sphere2 in self.collisions():
            if (sphere.rayon > sphere2.rayon * 3) or (sphere2.rayon > sphere.rayon * 3):
                if (sphere.durete < 6) and (sphere.rayon > sphere2.rayon):
                    absorption(sphere, sphere2)
                    ajouter_sphere_2 = False
                elif (sphere2.durete < 6) and (sphere2.rayon > sphere.rayon):
                    absorption(sphere, sphere2)
                    ajouter_sphere_1 = False
                else:
                    sphere.rebond()
                    sphere2.rebond()
            else:
                sphere.rebond()
                sphere2.rebond()
            for render in sphere.get_render_items() + sphere2.get_render_items():
                render.change_couleur()
            if ajouter_sphere_1:
                self.add_sphere(sphere)
            if ajouter_sphere_2:
                self.add_sphere(sphere2)