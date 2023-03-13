from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer
import sys
import traceback

class SphereItem(QGraphicsItem):
    """classe chargé de l'affichage d'une sphere, sous classe un QGraphicsItem, et est donc utiliseable dans un QGraphicsView"""
    def __init__(self, sphere:'PyBaseSphere') -> None:
        """initialise l'item de rendu lié a la sphere passé en argument

        Args:
            sphere (gravilib.PyBaseSphere): une sphere de type PyBaseSphere (ou dérivée)
        
        Methode Custom:
        update_pos(self) -> None: met a jour la position de l'item selon la position de la sphère
        """
        super().__init__()
        self.sphere: 'PyBaseSphere' = sphere
        self.radius: int = sphere.cy_sphere.get_coord()[3]
    def update_pos(self) -> None:
        """met a jour la position de l'item selon la position de la sphère"""
        self.setPos(*self.sphere.cy_sphere.get_coord()[0:2]) #(*list) == (list[0],list[1])
    
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
        self.setGeometry(100, 100, 800, 600)
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
            print("attempting to remove a graphic item who don't exist, please check the code")
            traceback.print_exc()
    
    def update_graph(self) -> None:
        """update le rendu de toute les sphères"""
        for item in self.scene.items():
            item.update_pos()

        self.view.setSceneRect(self.scene.itemsBoundingRect())