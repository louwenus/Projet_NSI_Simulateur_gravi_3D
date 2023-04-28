#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding = utf8

"""Ce fichier et composé de classes utilisé pour le rendu 3D des sphères :
Camera (gestion du point de vue)
SphereItem (affichage d'une sphère, lié a cette dernière)
Renderer3D (widget dans lequel le rendu est effectué)"""
import sys
import traceback
from typing import Callable

from PySide6.QtWidgets import QWidget,QLayout,QHBoxLayout
from PySide6.QtGui import QColor, QPen, QBrush, QPainter, QResizeEvent, QKeySequence
from PySide6.QtCore import Qt, QPointF
from math import cos, sin, sqrt

from . import settings


matrix3_3 = tuple[tuple[float, float, float],
                  tuple[float, float, float],
                  tuple[float, float, float]]

class Camera():
    def __init__(self, offsetX, offsetY, zoom:float=1, x:int=0, y:int=0, z:int=0, yaw:float=0, pitch:float=0, roll:float=0) -> None:
        """Camera attributes.

        Args:
            offsetX (float): devrait etre la moitié de la largeur de la fenetre
            offsetY (float): devrait etre la moitié de la hauteur de la fenetre
            zoom (float, optional): zoom initial, positif non-null. 1 par default.
            x (int, optional): abscisse initiale de la caméra. 0 par défault.
            y (int, optional): ordonnée initiale de la caméra. 0 par défault.
            z (int, optional): profondeur initiale de la caméra. 0 par défault.
            yaw (float, optional): Rotation de la caméra sur les abscisse. 0 par défault.
            pitch (float, optional): Rotation de la caméra sur les ordonnées. 0 par défault.
            roll (float, optional): Rotation de la caméra sur la profondeur. 0 par défault.
        """
        self.x: float = x
        self.y: float = y
        self.z: float = z

        self.yaw: float = yaw
        self.pitch: float = pitch
        self.roll: float = roll
        
        self.zoom:float = zoom
        
        self.offsetX:float = offsetX
        self.offsetY:float = offsetY
        
        self.update_matrix()


    def update_matrix(self) -> None:
        """Met à jour la matrice de rotation de la caméra."""
        # yaw = y,  pith = x,  roll = z
        #   yaw
        #[cos -sin 0] [cos  0 sin] [1  0   0  ]
        #[sin cos  0]*[ 0   1  0 ]*[0 cos -sin]
        #[ 0   0   1] [-sin 0 cos] [0 sin cos ]
        self.matrix: matrix3_3 = (
        (cos(self.yaw)*cos(self.roll) - sin(self.pitch)*sin(self.yaw)*sin(self.roll) , -cos(self.pitch)*sin(self.roll) , sin(self.pitch)*cos(self.yaw)*sin(self.roll) + sin(self.yaw)*cos(self.roll)),
        (sin(self.pitch)*sin(self.yaw)*cos(self.roll) + cos(self.yaw)*sin(self.roll) , cos(self.pitch)*cos(self.roll) ,  sin(self.yaw)*sin(self.roll) - sin(self.pitch)*cos(self.yaw)*cos(self.roll)),
        (-cos(self.pitch)*sin(self.yaw) ,                                              sin(self.pitch) ,                 cos(self.pitch)*cos(self.yaw)))


    def projection_sphere(self, coord: tuple[int, int, int], radius: int) -> tuple[tuple[float, float], float] | None:
        """Projette la sphère 3D sur l'écran de la caméra 2D.

        Args:
            coord (tuple[int,int,int]): Coordonnée de la sphère.
            radius (int): Radian de la sphère.

        Returns:
            tuple[tuple[float,float],float]: Un tuple des coordonnées de la projection et sa taille.
        """
        coord = (coord[0]-self.x, coord[1]-self.y, coord[2]-self.z)  # vecteur origine_camera/sphere
        coord_finale = (coord[0]*self.matrix[0][0] + coord[1]*self.matrix[0][1] + coord[2]*self.matrix[0][2],  # rotation du vecteur en fonction de l'orientation de la caméra
                 coord[0]*self.matrix[1][0] + coord[1]*self.matrix[1][1] + coord[2]*self.matrix[1][2],
                 coord[0]*self.matrix[2][0] + coord[1]*self.matrix[2][1] + coord[2]*self.matrix[2][2])
        
        if coord_finale[2] > 0:
            #x(0) vers la droite
            #y(1) vers le bas
            #z(2) vers le fond
            coord_plan: tuple[float, float] = (
                coord_finale[0]/coord_finale[2]*self.zoom*self.offsetX+self.offsetX,
                coord_finale[1]/coord_finale[2]*self.zoom*self.offsetX+self.offsetY)
            radius_plan: float = radius/coord_finale[2]*self.zoom*(self.offsetX+self.offsetY)
            
            return (coord_plan, radius_plan)      
        else:
            return None
    
    
    def move(self, cote:int=0, elev:int=0, profondeur:int=0):
        """deplace la caméra, avec cote, elev et profondeur en coordonées locales (tient compte de la rotation de la cam)"""
        cote/=self.zoom
        elev/=self.zoom
        profondeur/=self.zoom
        self.x += cote*self.matrix[0][0] + elev*self.matrix[1][0] + profondeur*self.matrix[2][0] 
        self.y += cote*self.matrix[0][1] + elev*self.matrix[1][1] + profondeur*self.matrix[2][1] 
        self.z += cote*self.matrix[0][2] + elev*self.matrix[1][2] + profondeur*self.matrix[2][2] 
        
        


class SphereItem():
    """Cette classe est chargée de l'affichage d'une sphere, a l'aide d'un painter passé a sa fonction paint"""
    
    def __init__(self, rayon: Callable[[], int], getcoords: Callable[[], tuple[int, int, int]], color: QColor) -> None:
        """Initialise un item de rendu sphérique de rayon fixe et faisant appel à la fonction getcoord pour update ses coordonées.

        Args:
            rayon (callable): doit renvoyer le rayon de la sphère lors de l'appel
            getcoord (callable): Une fonction renvoyant un tuple de coordonées entières x,y,z

        Methode Custom:
            paint(self,painter,camera): peint la boule sur le painter
            update_masse(self,masse:int): update la couleur de la boule selon la nouvelle masse
        """
        self.getcoords: Callable[[], tuple[int, int, int]] = getcoords
        self.radius: Callable[[], int] = rayon
        self.radius2D: float = 0
        self.pos = QPointF(0,0)
        self.color: QColor=color
        
    def paint(self, painter:QPainter, camera:Camera) -> None:
        """Permet de gérer le rendu graphique.

        Args:
            painter (class 'PySide6.QtGui.QPainter'): Permettant de modifier le rendu graphique.
        """
        statsDessin = camera.projection_sphere(self.getcoords(), self.radius())

        if statsDessin != None :
            coord2D, self.radius2D = statsDessin
            self.pos=QPointF(*coord2D)

            painter.setPen(QPen(QColor("black"),0.5))
            painter.setBrush(QBrush(self.color))

            painter.drawEllipse(self.pos, self.radius2D, self.radius2D)


class Renderer3D(QWidget):
    """ Widget chargée de l'affichage d'une dimmension ou plusieurs sphères.

    Méthode Custom:
    def add_to_display(self,item:SphereItem) -> None: ajoute l'item au graph
    def remove_from_display(self,item:SphereItem) -> None: retire l'item du graph
    def update_graph(self) -> None: appelle update_pos() sur tous les items du graph
    """

    def __init__(self,controlles) -> None:
        """Initialise le widget de rendu"""
        super().__init__()
        self.wid_con=controlles
        self.setFocusPolicy(Qt.ClickFocus)
        self.setGeometry(0,0,1000,800)
        self.mainlayout: QLayout = QHBoxLayout()
        self.setLayout(self.mainlayout)
        self.sphlist: list[SphereItem]=[]

        self.cam: Camera = Camera(offsetX=self.size().width()/2,
                                  offsetY=self.size().height()/2,
                                  zoom=settings.get("simulation.defaultzoom"),
                                  z=-100_000_000)
        self.reload_controlles()
        
        
    def paintEvent(self, paintEvent) -> None:
        """Met à jour et affiche la position des sphères.

        Args:
            paintEvent (class 'PySide6.QtGui.QPaintEvent'): évenement d'affichage des sphères.
        """
        painter = QPainter(self)
        
        for item in self.sphlist:
            
            try:
                item.paint(painter,self.cam)
                
            except:
                self.remove_from_display(item)
                if settings.get("logging")>=1:
                    print("an errored item was removed from display",file=sys.stderr)
                
        painter.end()


    def add_to_display(self, item: SphereItem) -> None:
        """Ajoute une sphère item à la liste des sphères présente.

        Args:
            item (SphereItem): SphereTem d'affichage3D.
        """
        self.sphlist.append(item)


    def remove_from_display(self, item: SphereItem) -> None:
        """Supprime la sphere.

        Args:
            item (SphereItem): SphereItem d'affichage3D
        """
        try:
            self.sphlist.remove(item)
            
        except:
            if settings.get("logging") == 1:
                print(
                    "Tentative de suppression d'un élément graphique qui n'existe pas. Augmentez la verbosité pour plus de détails.", file=sys.stderr)
                
            if settings.get("logging") >= 2:
                print(
                    "Tentative de suppression d'un objet qui n'existe pas, voir traceback", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)


    def wheelEvent(self, event):
        """Servznt à redéfinir l'angle de la caméra après un zoom / dézoom.

        Args:
            event (class 'PySide6.QtGui.QWheelEvent'): Evenement, ici molette de la souris.
        """
        y=event.angleDelta().y()
        if y > 100:
            self.cam.zoom*=1.3
            
        elif y<-100:
            self.cam.zoom/=1.3
        elif y>0:
            self.cam.zoom*=1+y/100*0.3
        else:
            self.cam.zoom/=1-y/100*0.3
            
            
    def reload_controlles(self,*any) -> None:
        """Sert à recharger les contrôles, claviers ou boutton ajouter.
        """
        self.controles: dict[str, QKeySequence]={
            "avancer":    QKeySequence(settings.get("simulation.controles.avancer")),
            "reculer":    QKeySequence(settings.get("simulation.controles.reculer")),
            "droite":     QKeySequence(settings.get("simulation.controles.droite")),
            "gauche":     QKeySequence(settings.get("simulation.controles.gauche")),
            "monter":     QKeySequence(settings.get("simulation.controles.monter")),
            "descendre":  QKeySequence(settings.get("simulation.controles.descendre")),
            "home":       QKeySequence(settings.get("simulation.controles.home")),
            "ajouter":    QKeySequence(settings.get("simulation.controles.ajouter")),
            "rot_haut":   QKeySequence(settings.get("simulation.controles.rot_haut")),
            "rot_bas":    QKeySequence(settings.get("simulation.controles.rot_bas")),
            "rot_gauche": QKeySequence(settings.get("simulation.controles.rot_gauche")),
            "rot_droite": QKeySequence(settings.get("simulation.controles.rot_droite")),
            "roul_gauche":QKeySequence(settings.get("simulation.controles.roul_gauche")),
            "roul_droite":QKeySequence(settings.get("simulation.controles.roul_droite")),
            "système_sol":QKeySequence(settings.get("simulation.controles.système_sol"))
        }
        
        
    def keyPressEvent(self, event):
        """ Modifie l'emplacement de la caméra.

        Args:
            event (class 'PySide6.QtGui.QKeyEvent'): Touche du clavier appuyée.
        """
         
        if event.keyCombination().toCombined() == self.controles["monter"]:
            """ Fait s'élever la camera de 50_000_000 metres"""
            self.cam.move(elev=-500_000/self.cam.zoom)
            
        if event.keyCombination().toCombined() == self.controles["descendre"]:
            """ Fait descendre la camera de 50_000_000 metres"""
            self.cam.move(elev=500_000)
            
        if event.keyCombination().toCombined() == self.controles["droite"]:
            """ Fait se décaler à droite la camera de 50_000_000 metres"""
            self.cam.move(cote=500_000)
            
        if event.keyCombination().toCombined() == self.controles["gauche"]:
            """ Fait se décaler à gauche la camera de 50_000_000 metres"""
            self.cam.move(cote=-500_000)
            
        if event.keyCombination().toCombined() == self.controles["avancer"]:
            """ Fait avancer la camera de 50_000_000 metres"""
            self.cam.move(profondeur=500_000)
            
        if event.keyCombination().toCombined() == self.controles["reculer"]:
            """ Fait reculer la camera de 5_000_000 km"""
            self.cam.move(profondeur=-500_000)
            
        if event.keyCombination().toCombined() == self.controles["home"]:
            """ Recentre et réinitialise la camera à ses valeurs de départ"""
            self.cam.x, self.cam.y, self.cam.z, self.cam.zoom = 0, 0, -5_000_000, settings.get("simulation.defaultzoom")
            self.cam.pitch, self.cam.roll, self.cam.yaw = 0, 0, 0
            self.cam.update_matrix()
            
        if event.keyCombination().toCombined() == self.controles["ajouter"]:
            "Ajoute des sphères"
            self.wid_con.ajouter_spheres(False)
        
        if event.keyCombination().toCombined() == self.controles["rot_haut"]:
            "fait tourner vers le haut"
            self.cam.pitch-=0.04/sqrt(self.cam.zoom)
            self.cam.update_matrix()

        if event.keyCombination().toCombined() == self.controles["rot_bas"]:
            "fait tourner vers le bas"
            self.cam.pitch+=0.04/sqrt(self.cam.zoom)
            self.cam.update_matrix()
        
        if event.keyCombination().toCombined() == self.controles["rot_gauche"]:
            "fait tourner vers la gauche"
            self.cam.yaw+=0.04/sqrt(self.cam.zoom)
            self.cam.update_matrix()
        
        if event.keyCombination().toCombined() == self.controles["rot_droite"]:
            "fait tourner vers la droite"
            self.cam.yaw-=0.04/sqrt(self.cam.zoom)
            self.cam.update_matrix()
        
        if event.keyCombination().toCombined() == self.controles["roul_gauche"]:
            "fait rouler vers la gauche"
            self.cam.roll+=0.01
            self.cam.update_matrix()
        
        if event.keyCombination().toCombined() == self.controles["roul_droite"]:
            "fait rouler vers la droite"
            self.cam.roll-=0.01
            self.cam.update_matrix()
    
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        """Décale la caméra par rapport au milieu de la fenêtre.

        Args:
            event (QResizeEvent): évenement de resize dans le widget.
        """
        self.cam.offsetX=self.size().width()/2
        self.cam.offsetY=self.size().height()/2