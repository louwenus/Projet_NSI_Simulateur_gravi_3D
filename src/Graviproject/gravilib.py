#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding = utf8
import sys
from math import sqrt
from random import randint
from . import affichage
from . import settings
try:
    from . import cppgravilib
    
except ModuleNotFoundError as e:
    print("cppravilib doit etre compilé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails.", file=sys.stderr)
    raise (e)

from .affichage3D import Renderer3D, SphereItem
ticktime=1
class PyBaseSphere(cppgravilib.CySimpleSphere):
    """classe utilisée pour gérer et collisioner les sphères.

    Args:
        cppgravilib (None): importe une CySimpleSphere de cppgravilib, permettant l'utilisation de cette dernière.
    """
    def __init__(self, x: int, y: int, z: int, masse: int, rayon: int, vx: int, vy: int, vz: int, d: int, ticktime:float) -> None:
        """Crée une PyBaseSphere sur la base d'une cySimpleSphere.

        Args:
            x,y,z (int): Position de départ de la sphère
            masse,rayon (int): Variable de la masse et du rayon de la sphère
            vx,vy,vz (int): Vitesse de départ de la sphère
            d (int) : Dureté de la sphère
        """
        self.durete = d
        ticktime:float=1/settings.get("simulation.fps")*settings.get("simulation.simspeed")
        self.init_c_container(x, y, z, masse, rayon, vx, vy, vz)
        self.set_ticktime(ticktime)
        self.render_item: SphereItem = SphereItem(
            self.get_rayon, self.get_coord,masse)
    
    def set_masse(self, masse: int) -> None:
        self.render_item.update_masse(masse)
        super().set_masse(masse)

    def get_render_items(self) -> list[SphereItem]:
        """Renvoie les items de SphereItem d'affichage3D

        Returns:
            list[SphereItem]: les items SphereItem pour pouvoir les manipuler par la suite.
        """
        return [self.render_item]


class PyBaseDimension(cppgravilib.CyBaseDimension):
    def __init__(self,render:Renderer3D,ticktime:float) -> None:
        self.init_c_container()
        self.render: Renderer3D=render #pour que l'on puisse utiliser self.render.remove_from_display(self, item: SphereItem)
        self.ticktime=ticktime
        
    def add_sphere(self, instance: cppgravilib.CyDummySphere) -> None:
        
        super().add_sphere(instance)

    def gerer_colision(self) -> None:
        """ Fonction s'occupant des collisions, faisant rebondir ou s'absorber 2 objet sphères de la class PyBaseSphere."""
        
        for sphere, sphere2 in self.collisions():
            vx1,vy1,vz1=sphere.get_speed()
            vx2,vy2,vz2=sphere2.get_speed()
            if (sphere.get_rayon() > sphere2.get_rayon() * 3) or (sphere2.get_rayon() > sphere.get_rayon() * 3):
                if (sphere.get_rayon() > sphere2.get_rayon() * 3):
                    absorption(sphere, sphere2)
                    self.add_sphere(sphere)
                    for render in sphere2.get_render_items():
                        self.render.remove_from_display(render)
                    """
                    if difference_energie(sphere):
                        explosion(sphere)
                        for render in sphere.get_render_items():
                           self.render.remove_from_display(render)"""# à revoir
                else:
                    absorption(sphere2, sphere)
                    self.add_sphere(sphere2)
                    for render in sphere.get_render_items():
                        self.render.remove_from_display(render)
                    """
                    if difference_energie(sphere2):
                        explosion(sphere2)
                        for render in sphere2.get_render_items():
                           self.render.remove_from_display(render)"""
                
            elif (vx1 + vy1 + vz1 - vx2 -vy2 -vz2)/3 < 50000000:
                transfert_v(sphere,sphere2)
                self.add_sphere(sphere)
                self.add_sphere(sphere2)
            elif sphere.durete < sphere2.durete:
                # changement de vitesse pour la sphère non explosé à implémenter
                explosion(sphere)
                for render in sphere.get_render_items():
                    self.render.remove_from_display(render)
                transfert_v(sphere2)
                self.add_sphere(sphere2)
            else:
                explosion(sphere2)
                for render in sphere2.get_render_items():
                    self.render.remove_from_display(render)
                transfert_v(sphere2)
                self.add_sphere(sphere)
    
def absorption (sphere1:PyBaseSphere, sphere2:PyBaseSphere):
    """ Fonction prenant en paramètre 2 sphères, et réalise l'absorption de la deuxiemme par la première
        Args:
            sphere1 (PyBaseSphere): sphere absorbante
            sphere2 (PyBaseSphere): sphere absorbé
    """
    
    volume: int=sphere1.get_rayon()**3
    volume +=(sphere2.get_rayon()**3)
    rayon =int(volume**(1/3))
    sphere1.set_rayon(rayon)
    m1 = sphere1.get_masse()
    m2 = sphere2.get_masse()
    masse_final: int= m1+m2
    vx1,vy1,vz1=sphere1.get_speed()
    vx2,vy2,vz2=sphere2.get_speed()
    vitessex = int((m1*vx1*2 + m2*vx2*2)/masse_final)   #gain (ou perte) de vitesse
    vitessey = int((m1*vy1*2 + m2*vy2*2)/masse_final)   #selon la formule moment cinétique = m*v
    vitessez = int((m1*vz1*2 + m2*vz2*2)/masse_final)
    sphere1.set_masse(masse_final)
    sphere1.set_speed((vitessex, vitessey, vitessez))

def difference_energie(sphere:PyBaseSphere):
    vx,vy,vz=sphere.get_speed()
    m = sphere.get_masse()
    energie_degagee = 0.5 * m * ((vx + vy + vz)/3)**2
    return energie_degagee/sphere.durete < 10**305

def explosion (sphere:PyBaseSphere):
    """Sépare la sphère en paramètre en plusieurs morceaux.

    Args:
        sphere (PyBaseSphere): classe PyBaseSphere de gravilib.py
    """
    vx,vy,vz=sphere.get_speed()
    d=sphere.durete
    m = sphere.get_masse()
    r = sphere.get_rayon()
    x,y,z = sphere.get_coord()
    nb_petit = randint(2,5)
    if int(round(m/nb_petit,0)) != 0:
        for _ in range (nb_petit):
            var = PyBaseSphere(x+_*r, y+_*r, z+_*r, int(round(m/nb_petit,0)) , int(round(r/nb_petit)), int(round(vx/2)), int(round(vy/2)), int(round(vz/2)), d, ticktime)
            affichage.Fenetre_principale.ajouter_sphere(var)
   
def transfer_e(sphere1:PyBaseSphere, sphere2:PyBaseSphere):
    """Prend en paramètre 2 sphères, calcul l'énergie libéré par leur collision et modifie les vitesses en conséquence.

    Args:
        sphere1 (PyBaseSphere): classe PyBaseSphere de gravilib.py
        sphere2 (PyBaseSphere): classe PyBaseSphere de gravilib.py
    """
    vx1,vy1,vz1=sphere1.get_speed()
    vx2,vy2,vz2=sphere2.get_speed()
    m1 = sphere1.get_masse()
    m2 = sphere2.get_masse()
    v_comx = (m1 * vx1 + m2 * vx2) / (m1 + m2)
    v_comy = (m1 * vy1 + m2 * vy2) / (m1 + m2)
    v_comz = (m1 * vz1 + m2 * vz2) / (m1 + m2)
    sphere1.set_speed((2 * m2 * v_comx - 2 * m1 * vx1) / (m1 + m2), (2 * m2 * v_comy - 2 * m1 * vy1) / (m1 + m2), (2 * m2 * v_comz - 2 * m1 * vz1) / (m1 + m2))
    sphere2.set_speed((2 * m1 * v_comx - 2 * m2 * vx2) / (m1 + m2), (2 * m1 * v_comy - 2 * m2 * vy2) / (m1 + m2), (2 * m1 * v_comz - 2 * m2 * vz2) / (m1 + m2))
    
def transfert_v(sphere1:PyBaseSphere, sphere2:PyBaseSphere):
    """Prend en paramètre 2 sphères et calcule le transfert de vitesse après impact."""
    
    d1=sphere1.durete
    d2=sphere2.durete
    m1=sphere1.get_masse()
    m2=sphere2.get_masse()
    
    vx1,vy1,vz1=sphere1.get_speed()
    vx2,vy2,vz2=sphere2.get_speed()
    
    e=(2*sqrt(d1*d2))/(d1+d2) #calcul de l'elasticité lors de la collision
    
    somme_m=m1+m2
    
    mvx1=m1*vx1
    mvx2=m2*vx2
    mvy1=m1*vy1
    mvy2=m2*vy2
    mvz1=m1*vz1
    mvz2=m2*vz2
    
    em1=e*m1
    em2=e*m2
    
    vfx1=int((mvx1+mvx2+em2*(vx2-vx1))/(somme_m))
    vfx2=int((mvx1+mvx2+em1*(vx1-vx2))/(somme_m))

    vfy1=int((mvy1+mvy2+em2*(vy2-vy1))/(somme_m))
    vfy2=int((mvy1+mvy2+em1*(vy1-vy2))/(somme_m))

    vfz1=int((mvz1+mvz2+em2*(vz2-vz1))/(somme_m))
    vfz2=int((mvz1+mvz2+em1*(vz1-vz2))/(somme_m)) #transfert de vitesses
    
    sphere1.set_speed((vfx1, vfy1, vfz1))
    sphere2.set_speed((vfx2, vfy2, vfz2))
