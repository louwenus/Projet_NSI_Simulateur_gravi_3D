#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding = utf8
import sys
from math import sqrt
from random import randint
from . import langue
from . import settings

try:
    from . import cppgravilib
except ModuleNotFoundError as e:
    print("cppravilib doit etre compilé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails.", file=sys.stderr)
    raise (e)

from .affichage3D import Renderer3D, SphereItem

if cppgravilib.is_128_bit:
    lighspeed=9_223_372_036_854_775_808 #lightspeed = numerical speed limit (64-bit signed C++ integer)
else:
    lighspeed=2_147_483_647 #lightspeed = numerical speed limit (32-bit signed C++ integer)

udPerMeter=int(lighspeed/299_792_458) #computing metter size based on lightspeed (c/lightspeed)
umPerKg=int((lighspeed/299_792_458)**3*(1/6.674_301_5)*10**11) #computing Kg weight based on udPerMeter and gravitation constant (c/lightspedd)³/G

class PyBaseSphere(cppgravilib.CySimpleSphere):
    """classe utilisée pour gérer et collisioner les sphères.

    Args:
        cppgravilib (None): importe une CySimpleSphere de cppgravilib, permettant l'utilisation de cette dernière.
    """
    def __init__(self, x: float, y: float, z: float, masse: float, rayon: float, vx: float, vy: float, vz: float, d: float, soft:bool=True) -> None:
        """Crée une PyBaseSphere sur la base d'une cySimpleSphere.

        Args:
            x,y,z (int): Position de départ de la sphère (en m)
            masse,rayon (int): Variable de la masse et du rayon de la sphère (en kg)
            vx,vy,vz (int): Vitesse de départ de la sphère (en m/s)
            d (int) : Dureté de la sphère
            soft (bool) : si les valeurs des args sont en m / kg ou en valeurs interne (ud/um). default en m et kg
        """
        self.durete: float = d
        if soft:
            self.init_c_container(x*udPerMeter, y*udPerMeter, z*udPerMeter, masse*umPerKg, rayon*udPerMeter, vx*udPerMeter, vy*udPerMeter, vz*udPerMeter)
        else:
            self.init_c_container(x, y, z, masse, rayon, vx, vy, vz)
        self.render_item: SphereItem = SphereItem(
            self.get_rayon, self.get_coord,masse)
    
    def set_masse(self, masse: float,soft=True) -> None:
        if soft:
            masse*=umPerKg
        self.render_item.update_masse(masse)
        super().set_masse(masse)
    def get_masse(self,soft=True) -> float:
        if soft:
            return super().get_masse()/umPerKg
        return super().get_masse()
    def get_coord(self,soft=True) -> tuple[float, float, float]:
        if soft:
            return tuple(c/udPerMeter for c in super().get_coord())
        return super().get_coord()
    def set_coord(self,coord:tuple[float,float,float],soft=True) -> None:
        if soft:
            super().set_coord(tuple(c*udPerMeter for c in coord))
        else:
            super().set_coord(coord)
    def get_speed(self,soft=True) -> tuple[float,float,float]:
        if soft:
            return tuple(s/udPerMeter for s in super().get_speed())
        return super().get_speed()
    def set_speed(self,speed:tuple[float,float,float],soft=True):
        if soft:
            super().set_speed(tuple(s*udPerMeter for s in speed))
        else :
            super().set_speed(speed)
    def get_rayon(self,soft=True) -> float:
        if soft:
            return super().get_rayon()/udPerMeter
        return super().get_rayon()
    def set_rayon(self,rayon:float,soft=True) -> None:
        if soft:
            super().set_rayon(rayon*udPerMeter)
        else:
            super().set_rayon(rayon)
    
    
    
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
        self.ticktime: float=ticktime
    def set_ticktime(self,ticktime:float) -> None:
        self.ticktime=ticktime
        for sphere in self.get_spheres():
            sphere.set_ticktime(ticktime)
    def add_sphere(self, instance: cppgravilib.CyDummySphere) -> None:
        instance.set_ticktime(self.ticktime)
        super().add_sphere(instance)

    def gerer_colision(self) -> None:
        """ Fonction s'occupant des collisions, faisant rebondir ou s'absorber 2 objet sphères de la class PyBaseSphere."""
        
        for sphere, sphere2 in self.collisions():
            vx1,vy1,vz1=sphere.get_energie()
            vx2,vy2,vz2=sphere2.get_energie()
            if (sphere.get_rayon() > sphere2.get_rayon() * 3) or (sphere2.get_rayon() > sphere.get_rayon() * 3):
                if (sphere.get_rayon() > sphere2.get_rayon() * 3):
                    self.absorption(sphere, sphere2)
                    self.add_sphere(sphere)
                    for render in sphere2.get_render_items():
                        self.render.remove_from_display(render)
                    if self.difference_energie(sphere):
                        self.explosion(sphere)
                        for render in sphere.get_render_items():
                           self.render.remove_from_display(render)
                else:
                    self.absorption(sphere2, sphere)
                    self.add_sphere(sphere2)
                    for render in sphere.get_render_items():
                        self.render.remove_from_display(render)
                    
                    if self.difference_energie(sphere2):
                        self.explosion(sphere2)
                        for render in sphere2.get_render_items():
                           self.render.remove_from_display(render)
                
            elif (vx1 + vy1 + vz1 - vx2 -vy2 -vz2)/3 < 50000000:
                self.transfert_v(sphere,sphere2)
                self.add_sphere(sphere)
                self.add_sphere(sphere2)
            elif sphere.durete < sphere2.durete:
                # changement de vitesse pour la sphère non explosé à implémenter
                self.explosion(sphere)
                for render in sphere.get_render_items():
                    self.render.remove_from_display(render)
                self.transfert_v(sphere,sphere2)
                self.add_sphere(sphere2)
            else:
                self.explosion(sphere2)
                for render in sphere2.get_render_items():
                    self.render.remove_from_display(render)
                self.transfert_v(sphere2,sphere)
                self.add_sphere(sphere)
    
    def absorption (self,sphere1:PyBaseSphere, sphere2:PyBaseSphere):
        """ Fonction prenant en paramètre 2 sphères, et réalise l'absorption de la deuxiemme par la première
            Args:
                sphere1 (PyBaseSphere): sphere absorbante
                sphere2 (PyBaseSphere): sphere absorbé
        """
        
        volume=sphere1.get_rayon()**3
        volume +=(sphere2.get_rayon()**3)
        rayon =volume**(1/3)
        sphere1.set_rayon(rayon)
        m1 = sphere1.get_masse()
        m2 = sphere2.get_masse()
        masse_final= m1+m2
        vx1,vy1,vz1=sphere1.get_energie()
        vx2,vy2,vz2=sphere2.get_energie()
        vitessex = (m1*vx1*2 + m2*vx2*2)/masse_final   #gain (ou perte) de vitesse
        vitessey = (m1*vy1*2 + m2*vy2*2)/masse_final   #selon la formule moment cinétique = m*v
        vitessez = (m1*vz1*2 + m2*vz2*2)/masse_final
        sphere1.set_masse(masse_final)
        sphere1.set_energie((vitessex, vitessey, vitessez))

    def difference_energie(self,sphere:PyBaseSphere) -> float:
        vx,vy,vz=sphere.get_energie()
        m = sphere.get_masse()
        energie_degagee = 0.5 * m * ((vx + vy + vz)/3)**2
        return energie_degagee/sphere.durete > 10**18

    def explosion (self,sphere:PyBaseSphere) -> None:
        """Sépare la sphère en paramètre en plusieurs morceaux.

        Args:
            sphere (PyBaseSphere): classe PyBaseSphere de gravilib.py
        """
        vx,vy,vz=sphere.get_energie()
        d=sphere.durete
        m = sphere.get_masse()
        r = sphere.get_rayon()
        x,y,z = sphere.get_coord()
        nb_petit = randint(2,5)
        if m/nb_petit >= 10**-10:
            for i in range (nb_petit):
                var = PyBaseSphere(x+i*r, y+i*r, z+i*r, m/nb_petit,0 , r/nb_petit, vx/2, vy/2, vz/2, d)
                for render in var.get_render_items():
                    self.render.add_to_display(render)
                self.add_sphere(var)
    
    def transfer_e(self,sphere1:PyBaseSphere, sphere2:PyBaseSphere) -> None:
        """Prend en paramètre 2 sphères, calcul l'énergie libéré par leur collision et modifie les vitesses en conséquence.

        Args:
            sphere1 (PyBaseSphere): classe PyBaseSphere de gravilib.py
            sphere2 (PyBaseSphere): classe PyBaseSphere de gravilib.py
        """
        vx1,vy1,vz1=sphere1.get_energie()
        vx2,vy2,vz2=sphere2.get_energie()
        m1 = sphere1.get_masse()
        m2 = sphere2.get_masse()
        v_comx = (m1 * vx1 + m2 * vx2) / (m1 + m2)
        v_comy = (m1 * vy1 + m2 * vy2) / (m1 + m2)
        v_comz = (m1 * vz1 + m2 * vz2) / (m1 + m2)
        sphere1.set_energie((2 * m2 * v_comx - 2 * m1 * vx1) / (m1 + m2), (2 * m2 * v_comy - 2 * m1 * vy1) / (m1 + m2), (2 * m2 * v_comz - 2 * m1 * vz1) / (m1 + m2))
        sphere2.set_energie((2 * m1 * v_comx - 2 * m2 * vx2) / (m1 + m2), (2 * m1 * v_comy - 2 * m2 * vy2) / (m1 + m2), (2 * m1 * v_comz - 2 * m2 * vz2) / (m1 + m2))
        
    def transfert_v(self,sphere1:PyBaseSphere, sphere2:PyBaseSphere):
        """Prend en paramètre 2 sphères et calcule le transfert de vitesse après impact."""
        
        d1=sphere1.durete
        d2=sphere2.durete
        m1=sphere1.get_masse()
        m2=sphere2.get_masse()
        
        vx1,vy1,vz1=sphere1.get_energie()
        vx2,vy2,vz2=sphere2.get_energie()
        
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
        
        vfx1=(mvx1+mvx2+em2*(vx2-vx1))/(somme_m)
        vfx2=(mvx1+mvx2+em1*(vx1-vx2))/(somme_m)

        vfy1=(mvy1+mvy2+em2*(vy2-vy1))/(somme_m)
        vfy2=(mvy1+mvy2+em1*(vy1-vy2))/(somme_m)

        vfz1=(mvz1+mvz2+em2*(vz2-vz1))/(somme_m)
        vfz2=(mvz1+mvz2+em1*(vz1-vz2))/(somme_m) #transfert de vitesses
        
        sphere1.set_energie((vfx1, vfy1, vfz1))
        sphere2.set_energie((vfx2, vfy2, vfz2))
