from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer
import sys
from . import gravilib

class SphereItem(QGraphicsItem):
    def __init__(self, sphere) -> None:
        super().__init__()
        self.sphere = sphere
        self.radius: int = sphere.get_coord()[3]

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

        self.sph: list[gravilib.PyBaseSphere]=[]
        
        self.sph.append(gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(1,1,1,0,10,10,20,20)))
        self.sph.append(gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(0,0,0,0,10,-10,-10,-10)))

        self.base_dimension: gravilib.cppgravilib.CyBaseDimension = gravilib.cppgravilib.CyBaseDimension()
        self.base_dimension.add_sphere(self.sph[0].cy_sphere)
        self.base_dimension.add_sphere(self.sph[1].cy_sphere)
        
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()

    def update_simulation(self) -> None:
        
        self.base_dimension.gravite_all(0.1)
        self.base_dimension.move_all(0.1)

        for item in self.scene.items():
            if isinstance(item, SphereItem):
                self.scene.removeItem(item)

        for sphere in self.sph:
            item: SphereItem = SphereItem(sphere)
            item.setPos(sphere.cy_sphere.get_coord()[0], sphere.cy_sphere.get_coord()[1])
            self.scene.addItem(item)

        self.view.setSceneRect(self.scene.itemsBoundingRect())