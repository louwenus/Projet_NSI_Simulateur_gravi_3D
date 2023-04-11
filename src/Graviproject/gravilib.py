import sys
from collections.abc import Iterable
from math import sqrt, pi
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
        #IL *NE* FAUT *PAS* FAIRE CA, ARRETEZ DE LE REMETTRE DANS LE CODE
        #et ne supprimez pas ce commentaire, il est la pour une raison
        #UTILISEZ self.get_speed() et self.set_speed((vx,vy,vz))
        #et de meme pour la masse, le rayon et la position, merci
        #self.vx,self.vy,self.vz=vx,vy,vz
        #self.masse=masse
        #self.rayon = rayon
        
        self.durete = d
        self.init_c_container(x, y, z, masse, rayon, vx, vy, vz)
        self.render_item: SphereItem = SphereItem(
            self.get_rayon, self.get_coord)
        if masse < 333000000:
            self.render_item.change_couleur(0)
        elif masse < 666000000:
            self.render_item.change_couleur(1)
        else:
            self.render_item.change_couleur(2)

    def get_render_items(self) -> list[SphereItem]:
        """renvoie les items de SphereItem d'affichage3D

        Returns:
            list[SphereItem]: les items SphereItem pour pouvoir les manipuler par la suite.
        """
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
            
            if (sphere.get_rayon() > sphere2.get_rayon() * 3):
                absorption(sphere, sphere2)
                self.add_sphere(sphere)
                for render in sphere2.get_render_items():
                    self.render.remove_from_display(render)
            elif (sphere2.get_rayon() > sphere.get_rayon() * 3):
                absorption(sphere2, sphere)
                self.add_sphere(sphere2)
                for render in sphere.get_render_items():
                    self.render.remove_from_display(render)
            else:
                transfert_v(sphere,sphere2)
                self.add_sphere(sphere)
                self.add_sphere(sphere2)
    
def absorption (sphere1:PyBaseSphere, sphere2:PyBaseSphere):
    """ Fonction prenant en paramètre 2 sphères, et réalise l'absorption de la deuxiemme par la première
        Args:
            sphere1 (PyBaseSphere): sphere absorbante
            sphere2 (PyBaseSphere): sphere absorbé
    """
    ratio_ajout = 1
    volume: int=sphere1.get_rayon()**3   #FUCK LES CONSTANTES
    volume    +=(sphere2.get_rayon()**3)/ratio_ajout
    rayon =int(volume**(1/3))
    sphere1.set_rayon(rayon)
    
    masse: int=sphere1.get_masse()
    masse    +=sphere2.get_masse()
    sphere1.set_masse(masse)


def transfert_v(sphere1:PyBaseSphere, sphere2:PyBaseSphere):
    """prend en paramètre 2 sphères et calcule le transfert de vitesse après impact"""
    d1=sphere1.durete
    d2=sphere2.durete
    m1=sphere1.get_masse()
    m2=sphere2.get_masse()
    vx1,vy1,vz1=sphere1.get_speed()
    vx2,vy2,vz2=sphere2.get_speed()
    e=(2*sqrt(d1*d2))/(d1+d2)
    somme_m=m1+m2
    mvx1=m1*vx1
    mvx2=m2*vx2
    mvy1=m1*vy1
    mvy2=m2*vy2
    mvz1=m1*vz1
    mvz2=m2*vz2
    em1=e*m1
    em2=e*m2    #sert à faire moins de calculs pour optimiser
    vfx1=int((mvx1+mvx2+em2*(vx2-vx1))/(somme_m))
    vfx2=int((mvx1+mvx2+em1*(vx1-vx2))/(somme_m))

    vfy1=int((mvy1+mvy2+em2*(vy2-vy1))/(somme_m))
    vfy2=int((mvy1+mvy2+em1*(vy1-vy2))/(somme_m))

    vfz1=int((mvz1+mvz2+em2*(vz2-vz1))/(somme_m))
    vfz2=int((mvz1+mvz2+em1*(vz1-vz2))/(somme_m))
    
    sphere1.set_speed((vfx1, vfy1, vfz1))
    sphere2.set_speed((vfx2, vfy2, vfz2))
