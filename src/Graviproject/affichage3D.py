from typing import Callable
import sys
import traceback
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer

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
    def update_pos(self) -> None:
        """met a jour la position de l'item selon la position de la sphère"""
        self.setPos(*self.getcoords()[0:2]) #(*list) == (list[0],list[1])
    
    def boundingRect(self) -> QRectF:
        return QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter, option, widget) -> None:
        painter.setPen(QPen(Qt.black, 0.5))
        painter.setBrush(QBrush(QColor(255, 0, 0, 128)))
        painter.drawEllipse(QPointF(0, 0), self.radius, self.radius)



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
        self.mainlayout: QLayout=QVBoxLayout()
        self.setLayout(self.mainlayout)
        
        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.view: QGraphicsView = QGraphicsView(self.scene)
        self.mainlayout.addWidget(self.view)
    
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
                print("attempting to remove a object that do not exist, see traceback")
                traceback.print_exc(file=sys.stderr)
    
    def update_graph(self) -> None:
        """update le rendu de toute les sphères"""
        if settings.get("logging")>=3:
            print("updating visual ...",end="")
        for item in self.scene.items():
            item.update_pos()

        self.view.setSceneRect(self.scene.itemsBoundingRect())
        if settings.get("logging")>=3:
            print("visual done!")