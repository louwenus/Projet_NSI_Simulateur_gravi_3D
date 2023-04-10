import sys
from collections.abc import Iterable
from math import sqrt
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
from .affichage3D import Renderer3D, SphereItem


class PyBaseSphere(cppgravilib.CySimpleSphere):
    def __init__(self, x: int, y: int, z: int, masse: int, rayon: int, vx: int, vy: int, vz: int, d: int) -> None:
        """crée une PyBaseSphere sur la base d'une cySimpleSphere

        Args:
            x,y,z (int): position de départ de la sphere
            masse,rayon (int): self-explicit
            vx,vy,vz (int): vitesse de départ de la sphère
            d (int) : dureté de la balle
        """
        self.vx,self.vy,self.vz=vx,vy,vz
        self.masse=masse
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


class PyBaseDimension(cppgravilib.CyBaseDimension):
    def __init__(self,render:Renderer3D) -> None:
        self.init_c_container()
        self.render: Renderer3D=render #so we can use self.render.remove_from_display(self, item: SphereItem)

    def gerer_colision(self) -> None:
        """ Fonction s'occupant des collisions, faisant rebondir ou s'absorber 2 objet sphere de la class PyBaseSphere
        """
        for sphere, sphere2 in self.collisions():
            transfert_v(sphere,sphere2)
            
            if (sphere.rayon > sphere2.rayon * 3) or (sphere2.rayon > sphere.rayon * 3):
                if (sphere.durete < 6) and (sphere.rayon > sphere2.rayon):
                    absorption(sphere, sphere2)
                elif (sphere2.durete < 6) and (sphere2.rayon > sphere.rayon):
                    absorption(sphere, sphere2)
                else:
                    sphere.rebond()
                    sphere2.rebond()
            else:
                sphere.rebond()
                sphere2.rebond()
            for render in sphere.get_render_items() + sphere2.get_render_items():
                render.change_couleur()
                self.render.remove_from_display(render)
            #self.add_sphere(sphere)
            #self.add_sphere(sphere2)
    
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
        #for render in sphere2.get_render_items():
        #    render.disparaitre()
    else:
        for render in sphere2.get_render_items():
            render.grossir(vol_1/5)
        #for render in sphere1.get_render_items():
        #    render.disparaitre()
def transfert_v(sphere1:PyBaseSphere, sphere2:PyBaseSphere):
    """prend en paramètre 2 sphères et calcule le transfert de vitesse après impact"""
    d1=sphere1.durete*1000
    d2=sphere2.durete*1000
    m1=sphere1.masse*1000
    m2=sphere2.masse*1000
    vx1,vy1,vz1=sphere1.vx*1000,sphere1.vy*1000,sphere1.vz*1000
    vx2,vy2,vz2=sphere2.vx*1000,sphere2.vy*1000,sphere2.vz*1000
    e=(2*sqrt(d1*d2))/(d1+d2)
    vfx1=(m1*vx1+m2*vx2+e*m2*(vx2-vx1))//(m1+m2)
    vfx2=(m1*vx1+m2*vx2+e*m1*(vx1-vx2))//(m1+m2)

    vfy1=(m1*vy1+m2*vy2+e*m2*(vy2-vy1))//(m1+m2)
    vfy2=(m1*vy1+m2*vy2+e*m1*(vy1-vy2))//(m1+m2)

    vfz1=(m1*vz1+m2*vz2+e*m2*(vz2-vz1))//(m1+m2)
    vfz2=(m1*vz1+m2*vz2+e*m1*(vz1-vz2))//(m1+m2)
    
    sphere1.set_speed((vfx1, vfy1, vfz1))
    sphere2.set_speed((vfx2, vfy2, vfz2))
