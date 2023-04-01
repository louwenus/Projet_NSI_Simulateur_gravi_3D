from typing import Callable
from random import *
import sys
import traceback
import types
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer
from math import cos, sin

from . import settings




class Camera():
    def __init__(self, x:int=0, y:int=0, z:int=0, yaw:float=0, pitch:float=0, roll:float=0) -> None:
        """Camera attributes.

        Args:
            x (int, optional): x coordinate of the camera. Defaults to 0.
            y (int, optional): y coordinate of the camera. Defaults to 0.
            z (int, optional): z coordinate of the camera. Defaults to 0.
            yaw (float, optional): Rotation of the camera on the x axis. Defaults to 0.
            pitch (float, optional): Rotation of the camera on the y axis. Defaults to 0.
            roll (float, optional): Rotation of the camera on the z axis. Defaults to 0.
        """
        self.x: int=x
        self.y: int=y
        self.z: int=z
        
        self.yaw: float=yaw
        self.pitch: float=pitch
        self.roll: float=roll
        
        self.matrix_rotation()
        
        
    def matrix_rotation(self) -> None:
        """Updates the rotation matrix of the camera.
        """
        matrix3_3=tuple[tuple[float,float,float],tuple[float,float,float],tuple[float,float,float]]
        
        self.matrix:matrix3_3=((  cos(self.yaw) * cos(self.pitch)  ,  cos(self.yaw) * sin(self.pitch) * sin(self.roll) - sin(self.yaw) * cos(self.roll)  ,  cos(self.yaw) * sin(self.pitch) * cos(self.roll) + sin(self.yaw) * sin(self.roll)  ),
                               (  sin(self.yaw) * cos(self.pitch)  ,  sin(self.yaw) * sin(self.pitch) * sin(self.roll) + cos(self.yaw) * cos(self.roll)  ,  sin(self.yaw) * sin(self.pitch) * cos(self.roll) - cos(self.yaw) * sin(self.roll)  ),
                               (          -sin(self.pitch)         ,                           cos(self.pitch) * sin(self.roll)                          ,                           cos(self.pitch) * cos(self.roll)                          ))
    
    
    def projection_sphere(self, coord:tuple[int,int,int], radius:int) -> tuple[tuple[float,float],float]:
        """Projects the 3D sphere onto the 2D camera screen.

        Args:
            coord (tuple[int,int,int]): Coordinates of the sphere.
            radius (int): Radius of the sphere.

        Returns:
            tuple[tuple[float,float],float]: A tuple of the coordinates of the projection and its size.
        """
        coord=(coord[0]-self.x , coord[1]-self.y , coord[2]-self.z) # vecteur origine_camera/sphere
        coord=(coord[2] * self.matrix[0][2] + coord[1] * self.matrix[0][1] + coord[0] * self.matrix[0][0] , # rotation du vecteur en fonction de l'orientation de la caméra
               coord[2] * self.matrix[1][2] + coord[1] * self.matrix[1][1] + coord[0] * self.matrix[1][0] ,
               coord[2] * self.matrix[2][2] + coord[1] * self.matrix[2][1] + coord[0] * self.matrix[2][0])
        if coord[2]>0:
            coord_plan:tuple[float,float] = (coord[0]/coord[2],coord[1]/coord[2])
            radius_plan:float = radius/coord[2]
        else:
            coord_plan:tuple[float,float] = (0,0)
            radius_plan:float = 0
        
        return (coord_plan, radius_plan)




class SphereItem(QGraphicsItem):
    """classe chargé de l'affichage d'une sphere, sous classe un QGraphicsItem, et est donc utiliseable dans un QGraphicsView"""
    def __init__(self, rayon:int, getcoords:Callable[[],tuple[int,int,int]]) -> None:
        """initialise un item de rendu sphérique de rayon fixe et faisant appel a la fonction getcoord pour update ses coordonées

        Args:
            rayon (int): le rayon de la sphère
            getcoord (function): une fonction renvoyant un tuple de coordonées entières x,y,z
        
        Methode Custom:
        update_pos(self) -> None: met a jour la position de l'item selon la position de la sphère
        """
        super().__init__()
        self.getcoords: Callable[[],tuple[int,int,int]] = getcoords
        self.radius: int = rayon
        self.radius2D:float = 0
        self.compteur = 0
        self.couleur = ["red", "green", "purple", "blue", "yellow"]
        
        
    def update_pos(self,camera:Camera) -> None:
        """met a jour la position de l'item selon la position de la sphère"""
        coord:tuple[int, int, int] = self.getcoords()
        
        parameter2D=camera.projection_sphere(coord,self.radius)
        self.radius2D=parameter2D[1]
        coord2D=parameter2D[0]
        
        self.setPos(*coord2D)
    
    
    def boundingRect(self) -> QRectF:
        return QRectF(-1*self.radius2D, -1*self.radius2D, 2 * self.radius2D, 2 * self.radius2D)


    def paint(self, painter, option, widget) -> None:
        
        painter.setPen(QPen(Qt.black, 0.5))
        painter.setBrush(QBrush(self.couleur[self.compteur]))
        
        painter.drawEllipse(QPointF(0, 0), self.radius2D, self.radius2D)


    def change_couleur (self):
        self.compteur = randint(1,4)
        



class Renderer3D(QWidget):
    """ Widget chargée de l'affichage d'une dimmension (plusieurs sphères)
    
    Methode Custom:
    def add_to_display(self,item:SphereItem) -> None: ajoute l'item au graph
    def remove_from_display(self,item:SphereItem) -> None: retire l'item du graph
    def update_graph(self) -> None: appelle update_pos() sur tous les items du graph
    """
    def __init__(self) -> None:
        """initialise le widget de rendu"""
        super().__init__()
        #self.setGeometry(100, 100, 800, 600)
        self.mainlayout:QLayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        
        self.scene:QGraphicsScene = QGraphicsScene(self)
        self.view:QGraphicsView = QGraphicsView(self.scene)
        #self.view.setUpdatesEnabled(False)
        zoom:float=settings.get("simulation.defaultzoom")
        self.view.scale(zoom,zoom)
        def wheel_ignore(object,event):
            event.ignore()
        self.view.wheelEvent=types.MethodType(wheel_ignore,QGraphicsView)
        self.mainlayout.addWidget(self.view)
        
        self.cam:Camera = Camera()
    
    
    def add_to_display(self,item:SphereItem) -> None:
        self.scene.addItem(item)
        self.view.setSceneRect(self.scene.itemsBoundingRect())
        
        
    def remove_from_display(self,item:SphereItem) -> None:
        try:
            self.scene.removeItem(item)
        except:
            if settings.get("logging")==1:
                print("attempting to remove a graphic item who don't exist. Augment verbosity for more details.",file=sys.stderr)
            if settings.get("logging")>=2:
                print("attempting to remove a object that do not exist, see traceback",file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
    
    
    def update_graph(self) -> None:
        """update le rendu de toute les sphères"""
        
        #print(self.view.size())
        
        if settings.get("logging")>=3:
            print("updating visual ...",end="")
        for item in self.scene.items():
            item.update_pos(self.cam)
        self.view.update()
        self.view.setSceneRect(self.scene.itemsBoundingRect())
        if settings.get("logging")>=3:
            print("visual done!")
    
        self.view.wheelEvent


    def wheelEvent(self, event):
        if event.angleDelta().y()>0:
            self.view.scale(1.25,1.25)
        else:
            self.view.scale(0.75,0.75)