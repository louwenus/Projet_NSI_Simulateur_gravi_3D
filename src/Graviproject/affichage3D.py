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
        self.compteur = 0
        self.couleur = ["red", "green", "purple", "blu", "black"]
    def update_pos(self,camera) -> None:
        """met a jour la position de l'item selon la position de la sphère"""
        coord: tuple[int, int, int]=self.getcoords()
        coord=(coord[0]-camera[0],coord[1]-camera[1],coord[2]-camera[2]) # vecteur origine_camera/sphere
        #compo_cam:tuple[int,int,int]=(coord[0]*camera[3],coord[1]*camera[4],coord[2]*camera[5])
        
        self.setPos(*coord[0:2]) #(*list) == (list[0],list[1])
    
    def boundingRect(self) -> QRectF:
        return QRectF(-1*self.radius, -1*self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter, option, widget) -> None:
        
        painter.setPen(QPen(Qt.black, 0.5))
        painter.setBrush(QBrush(self.couleur[self.compteur]))
        
        painter.drawEllipse(QPointF(0, 0), self.radius, self.radius)

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
        
        self.camera:tuple[int,int,int,int,int,int] = (0,0,0,1,0,0) # (vecteur_pos,vecteur_rot)
    
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
            item.update_pos(self.camera)
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
        self.x=x
        self.y=y
        self.z=z
        
        self.yaw=yaw
        self.pitch=pitch
        self.roll=roll
        
        self.matrix_rotation()
        
    def matrix_rotation(self) -> None:
        """Updates the rotation matrix of the camera.
        """
        matrix3_3=tuple[tuple[float,float,float],tuple[float,float,float],tuple[float,float,float]]
        
        self.matrix:matrix3_3=((  cos(self.yaw) * cos(self.pitch)  ,  cos(self.yaw) * sin(self.pitch) * sin(self.roll) - sin(self.yaw) * cos(self.roll)  ,  cos(self.yaw) * sin(self.pitch) * cos(self.roll) + sin(self.yaw) * sin(self.roll)  ),
                               (  sin(self.yaw) * cos(self.pitch)  ,  sin(self.yaw) * sin(self.pitch) * sin(self.roll) + cos(self.yaw) * cos(self.roll)  ,  sin(self.yaw) * sin(self.pitch) * cos(self.roll) - cos(self.yaw) * sin(self.roll)  ),
                               (          -sin(self.pitch)         ,                           cos(self.pitch) * sin(self.roll)                          ,                           cos(self.pitch) * cos(self.roll)                          ))
        
    def bidul(self, item:SphereItem):
        coord:tuple[int, int, int] = item.getcoords()
        coord=(coord[0]-self.x , coord[1]-self.y , coord[2]-self.z) # vecteur origine_camera/sphere
        coord=(coord[2] * self.matrix[0][2] + coord[1] * self.matrix[0][1] + coord[0] * self.matrix[0][0]  ,  coord[2] * self.matrix[1][2] + coord[1] * self.matrix[1][1] + coord[0] * self.matrix[1][0]  ,  coord[2] * self.matrix[2][2] + coord[1] * self.matrix[2][1] + coord[0] * self.matrix[2][0])
        
        coord_plan=(coord[0]/coord[2],coord[1]/coord[2])
        radius_plan=item.radius/coord[2]
        
        return (coord_plan, radius_plan)