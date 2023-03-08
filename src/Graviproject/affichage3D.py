from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer
import sys
import traceback

class SphereItem(QGraphicsItem):
    def __init__(self, sphere) -> None:
        super().__init__()
        self.sphere = sphere
        self.radius: int = sphere.cy_sphere.get_coord()[3]
    def update_pos(self) -> None:
        self.setPos(*self.sphere.cy_sphere.get_coord()[0:2]) #(*list) == (list[0],list[1])
    
    def boundingRect(self) -> QRectF:
        return QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter, option, widget) -> None:
        painter.setPen(QPen(Qt.black, 0.5))
        painter.setBrush(QBrush(QColor(255, 0, 0, 128)))
        painter.drawEllipse(QPointF(0, 0), self.radius, self.radius)

class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.view: QGraphicsView = QGraphicsView(self.scene)
        #self.setCentralWidget(self.view)
        self.mainlayout: QLayout=QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.view)

        self.itemlist: list[QGraphicsItem]=[]
        
        #self.sph.append(gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(1,1,1,0,10,10,20,20)))
        #self.sph.append(gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(0,0,0,0,10,-10,-10,-10)))

        #self.base_dimension: gravilib.cppgravilib.CyBaseDimension = gravilib.cppgravilib.CyBaseDimension()
        #self.base_dimension.add_sphere(self.sph[0].cy_sphere)
        #self.base_dimension.add_sphere(self.sph[1].cy_sphere)
        
        #self.timer: QTimer = QTimer(self)
        #self.timer.setInterval(10)
        #self.timer.timeout.connect(self.update_simulation)
        #self.timer.start()
    
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
        
        #self.base_dimension.gravite_all(0.1)
        #self.base_dimension.move_all(0.1)

        for item in self.scene.items():
            item.update_pos()

        #for sphere in self.sph:
        #    item: SphereItem = SphereItem(sphere)
        #    item.setPos(sphere.cy_sphere.get_coord()[0], sphere.cy_sphere.get_coord()[1])
        #    self.scene.addItem(item)

        self.view.setSceneRect(self.scene.itemsBoundingRect())