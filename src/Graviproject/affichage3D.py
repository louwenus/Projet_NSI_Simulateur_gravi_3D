#Importation des librairies et modules
#Ceci est une ligne inutile pour que mes camarades null puissent faire fonctionner ce ptn de programme de ces morts
from typing import Callable
from random import *
import sys
import traceback
import types
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QPen, QBrush, QPainter, QResizeEvent, QKeySequence
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer
from math import cos, sin

from . import settings
""" Import des fonctions, attributs... utilisez dans le projet."""




class Camera():
    def __init__(self, zoom:float=1, offsetX:float=0, offsetY:float=0, x:int=0, y:int=0, z:int=0, yaw:float=0, pitch:float=0, roll:float=0) -> None:
        """Camera attributes.

        Args:
            x (int, optional): x abscisse de la caméra. 0 par défault.
            y (int, optional): y ordonnée de la caméra. 0 par défault.
            z (int, optional): z profondeur de la caméra. 0 par défault.
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
        matrix3_3 = tuple[tuple[float, float, float],
                          tuple[float, float, float],
                          tuple[float, float, float]]

        self.matrix: matrix3_3 = ((cos(self.yaw)*cos(self.pitch),  cos(self.yaw)*sin(self.pitch)*sin(self.roll) - sin(self.yaw)*cos(self.roll),  cos(self.yaw)*sin(self.pitch)*cos(self.roll) + sin(self.yaw)*sin(self.roll)),
                                  (sin(self.yaw)*cos(self.pitch),  sin(self.yaw)*sin(self.pitch)*sin(self.roll) + cos(self.yaw)*cos(self.roll),  sin(self.yaw)*sin(self.pitch)*cos(self.roll) - cos(self.yaw)*sin(self.roll)),
                                  (-sin(self.pitch),               cos(self.pitch)*sin(self.roll),                                               cos(self.pitch)*cos(self.roll)))


    def projection_sphere(self, coord: tuple[int, int, int], radius: int) -> tuple[tuple[float, float], float]:
        """Projette la sphère 3D sur l'écran de la caméra 2D.

        Args:
            coord (tuple[int,int,int]): Coordonnée de la sphère.
            radius (int): Radian de la sphère.

        Returns:
            tuple[tuple[float,float],float]: Un tuple des coordonnées de la projection et sa taille.
        """
        coord = (coord[0]-self.x, coord[1]-self.y, coord[2]-self.z)  # vecteur origine_camera/sphere
        coord = (coord[2]*self.matrix[0][2] + coord[1]*self.matrix[0][1] + coord[0]*self.matrix[0][0],  # rotation du vecteur en fonction de l'orientation de la caméra
                 coord[2]*self.matrix[1][2] + coord[1]*self.matrix[1][1] + coord[0]*self.matrix[1][0],
                 coord[2]*self.matrix[2][2] + coord[1]*self.matrix[2][1] + coord[0]*self.matrix[2][0])
        
        if coord[2] > 1:
            coord_plan: tuple[float, float] = (
                coord[0]/coord[2]*self.zoom+self.offsetX, coord[1]/coord[2]*self.zoom+self.offsetY)
            radius_plan: float = radius/coord[2]*self.zoom
            
        else:
            #Améliorable ?
            coord_plan: tuple[float, float] = (0, 0)
            radius_plan: float = 0

        return (coord_plan, radius_plan)
    
    
    def move(self, cote:int=0, elev:int=0, profondeur:int=0):

        self.x += profondeur*self.matrix[0][2] + elev*self.matrix[0][1] + cote*self.matrix[0][0]
        self.y += profondeur*self.matrix[1][2] + elev*self.matrix[1][1] + cote*self.matrix[1][0]
        self.z += profondeur*self.matrix[2][2] + elev*self.matrix[2][1] + cote*self.matrix[2][0]
        
        


class SphereItem():
    """Cette classe est chargée de l'affichage d'une sphere, sous classe un QGraphicsItem, et est donc utiliseable dans un QGraphicsView"""
    couleur = ["darkorange", "cyan", "lime"]
    
    def __init__(self, rayon: Callable[[], int], getcoords: Callable[[], tuple[int, int, int]]) -> None:
        """Initialise un item de rendu sphérique de rayon fixe et faisant appel à la fonction getcoord pour update ses coordonées.

        Args:
            rayon (int): le rayon de la sphère
            getcoord (function): Une fonction renvoyant un tuple de coordonées entières x,y,z

        Methode Custom:
        update_pos(self) -> None: Met à jour la position de l'item selon la position de la sphère
        """
        super().__init__()
        self.getcoords: Callable[[], tuple[int, int, int]] = getcoords
        self.radius: Callable[[], int] = rayon
        self.radius2D: float = 0
        self.compteur: int = 0
        self.pos = QPointF(0,0)


    def update_pos(self, camera: Camera) -> None:
        """Met à jour la position de l'item selon la position de la sphère"""

        coord2D, self.radius2D = camera.projection_sphere(self.getcoords(), self.radius())

        self.pos=QPointF(*coord2D)


    def paint(self, painter) -> None:
        """Permet de gérer le rendu graphique.

        Args:
            painter (class 'PySide6.QtGui.QPainter'): Permettant de modifier le rendu graphique.
        """
        painter.setPen(QPen(Qt.black, 0.5))
        painter.setBrush(QBrush(self.couleur[self.compteur]))

        painter.drawEllipse(self.pos, self.radius2D, self.radius2D)


    def change_couleur(self, indice):
        """ Modifie la couleur de la sphere en une couleur prédéfinie de la liste couleur."""
        self.compteur = indice




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

        zoom: float = settings.get("simulation.defaultzoom")
        
        self.cam: Camera = Camera(zoom=zoom, offsetX=self.size().width()/2, offsetY=self.size().height()/2)
        self.reload_controlles()
        
        
    def paintEvent(self, paintEvent) -> None:
        """Met à jour et affiche la position des sphères.

        Args:
            paintEvent (class 'PySide6.QtGui.QPaintEvent'): évenement d'affichage des sphères.
        """
        painter = QPainter(self)
        
        for item in self.sphlist:
            
            try:
                item.update_pos(self.cam)
                item.paint(painter)
                
            except:
                self.remove_from_display(item)
                
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
        if event.angleDelta().y() > 0:
            self.cam.zoom*=1.25
            
        else:
            self.cam.zoom*=0.75
            
            
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
            "roul_droite":QKeySequence(settings.get("simulation.controles.roul_droite"))
        }
        
        
    def keyPressEvent(self, event):
        """ Modifie l'emplacement de la caméra.

        Args:
            event (class 'PySide6.QtGui.QKeyEvent'): Touche du clavier appuyée.
        """
         
        if event.key() == self.controles["monter"]:
            """ Fait s'élever la camera de 100000000 px"""
            self.cam.move(elev=-100000000)
            
        if event.key() == self.controles["descendre"]:
            """ Fait descendre la camera de 100000000 px"""
            self.cam.move(elev=100000000)
            
        if event.key() == self.controles["droite"]:
            """ Fait se décaler à droite la camera de 100000000 px"""
            self.cam.move(cote=100000000)
            
        if event.key() == self.controles["gauche"]:
            """ Fait se décaler à gauche la camera de 100000000 px"""
            self.cam.move(cote=-100000000)
            
        if event.key() == self.controles["avancer"]:
            """ Fait avancer la camera de 100000000 px"""
            self.cam.move(profondeur=100000000)
            
        if event.key() == self.controles["reculer"]:
            """ Fait reculer la camera de 100000000 px"""
            self.cam.move(profondeur=-100000000)
            
        if event.key() == self.controles["home"]:
            """ Recentre et réinitialise la camera à ses valeurs de départ"""
            self.cam.x, self.cam.y, self.cam.z, self.cam.zoom = 0, 0, 0, settings.get("simulation.defaultzoom")
            self.cam.pitch, self.cam.roll, self.cam.yaw = 0, 0, 0
            self.cam.update_matrix()
            
        if event.key() == self.controles["ajouter"]:
            "Ajoute des sphères"
            self.wid_con.ajouter_spheres(False)
        
        if event.key() == self.controles["rot_haut"]:
            "fait tourner vers le haut de 0.1 radian"
            self.cam.roll-=0.1
            self.cam.update_matrix()

        if event.key() == self.controles["rot_bas"]:
            "fait tourner vers le bas de 0.1 radian"
            self.cam.roll+=0.1
            self.cam.update_matrix()
        
        if event.key() == self.controles["rot_gauche"]:
            "fait tourner vers la gauche de 0.1 radian"
            self.cam.pitch+=0.1
            self.cam.update_matrix()
        
        if event.key() == self.controles["rot_droite"]:
            "fait tourner vers la droite de 0.1 radian"
            self.cam.pitch-=0.1
            self.cam.update_matrix()
        
        if event.key() == self.controles["roul_gauche"]:
            "fait rouler vers la gauche de 0.1 radian"
            self.cam.yaw-=0.1
            self.cam.update_matrix()
        
        if event.key() == self.controles["roul_droite"]:
            "fait rouler vers la droite de 0.1 radian"
            self.cam.yaw+=0.1
            self.cam.update_matrix()
    
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        """Décale la caméra par rapport au milieu de la fenêtre.

        Args:
            event (QResizeEvent): évenement de resize dans le widget.
        """
        self.cam.offsetX=self.size().width()/2
        self.cam.offsetY=self.size().height()/2