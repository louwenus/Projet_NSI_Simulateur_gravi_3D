#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8


from . import settings
import sys
from sys import stderr
try:
    # import PySide6
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from random import *
except ModuleNotFoundError as e:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails", file=stderr)
    raise e
from . import gravilib
from .affichage3D import SphereItem, Renderer3D

import os

from time import time

app: QApplication = QApplication(sys.argv)


class Main_window(QWidget):
    """Définit la fenètre principale du programme, à partir d'un QWidget."""

    def __init__(self) -> None:
        super().__init__()
        self.affichage_controles: bool = True

        self.setWindowTitle("Affichage")

        self.layout: QLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addSpacing(10)

        # creation des actions utiliseables dans les menus
        self.attach_detachAction: QAction = QAction(
            "&Détacher les contrôles", self)
        self.attach_detachAction.triggered.connect(
            self.attach_detach_controles)

        self.licenseAction: QAction = QAction("&Lire la license", self)
        self.licenseAction.triggered.connect(self.affich_licence)

        # création des menus
        self.menuBar: QWidget = QMenuBar(self)
        self.menuBar.setFixedWidth(self.size().width())

        self.affichageMenu: QMenu = QMenu("&Affichage", self.menuBar)
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.attach_detachAction)

        self.helpMenu: QMenu = QMenu("&Help", self.menuBar)
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(self.licenseAction)

        # fenettre détacheable de controle
        self.affichage_controles: bool = True
        self.controles = Controles()
        self.layout.addWidget(self.controles)

        # widget de rendu3D
        self.widget_3D: Renderer3D = Renderer3D()
        self.layout.addWidget(self.widget_3D)

        # dimension affiché par la fennettre de rendu
        self.dimension = gravilib.PyBaseDimension()
        # a raffiner, mais est utilisé pour update la simulation toute les 10ms
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()
        if settings.get("logging") >= 2:
            print("main windows initialized")


    def closeEvent(self, event) -> None:
        # Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme
        app.exit(0)
        
    def keyPressEvent(self, event):
        #à commenter
        if event.key() == Qt.Key_Escape:
            app.exit(0)
        
        if event.key() == Qt.Key_Z:
           self.widget_3D.mvCam("u")
        if event.key() == Qt.Key_S:
            self.widget_3D.mvCam("d")
        if event.key() == Qt.Key_Q:
            self.widget_3D.mvCam("l")
        if event.key() == Qt.Key_D:
            self.widget_3D.mvCam("r")
            
    def attach_detach_controles(self) -> None:
        if self.affichage_controles:
            self.controles.hide()
            controles_graphiques.show()
            self.attach_detachAction.setText("&Attacher les contrôles")
            self.affichage_controles = False
            if settings.get("logging") >= 2:
                print("controles déttachés")
        else:
            self.controles.show()
            controles_graphiques.hide()
            self.attach_detachAction.setText("&Détacher les contrôles")
            self.affichage_controles = True
            if settings.get("logging") >= 2:
                print("controles attachés")

    def affich_licence(self) -> None:
        self.fenetre_license: QWidget = QScrollArea()
        self.fenetre_license.setWindowTitle("LICENSE")

        try:
            path: str = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(path, "LICENSCE_FR")
            with open(path) as file:
                self.licenseTextlabel: QWidget = QLabel(file.read())
        except:
            if settings.get("logging") >= 1:
                print("The french licence file was not found at", path, file=stderr)
            self.licenseTextlabel: QWidget = QLabel(
                "Ficher manquant ou chemin cassé.\n\nRendez vous sur :\nhttps://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D/blob/main/LICENSCE_FR")

        self.fenetre_license.setWidget(self.licenseTextlabel)
        self.fenetre_license.show()

    def ajouter_sphere(self, sph: gravilib.PyBaseSphere) -> None:
        self.dimension.add_sphere(sph)
        for rendu in sph.get_render_items():
            self.widget_3D.add_to_display(rendu)

    def update_simulation(self) -> None:
        totalstart = time()
        start = time()
        print("starting update")
        self.dimension.gravite_all(0.1)
        print("grav time:", time()-start)
        start = time()
        self.dimension.move_all(0.1)
        print("move time:", time()-start)
        start = time()
        self.dimension.gerer_colision()
        print("coli time", time()-start)
        start = time()
        self.widget_3D.repaint()
        print("graph time:", time()-start)
        print("total:", time()-totalstart)
        # sphere : gravilib.PyBaseSphere
        # for sphere in self.dimension.get_spheres():
        #    pass

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.menuBar.setFixedWidth(self.size().width())
        return super().resizeEvent(event)


class Controles(QWidget):
    fenetre_ajoute: QWidget = QScrollArea()
    fenetre_ajoute.setWindowTitle("Ajoutez des sphères !")
    layout_aj_sph: QLayout = QFormLayout()
    fenetre_ajoute.setLayout(layout_aj_sph)

    amount = QSpinBox(minimum=0, maximum=1000, value=100)
    result_label = QLabel('')
    layout_aj_sph.addRow('nb sphères:', amount)
    layout_aj_sph.addRow(result_label)

    xmax = QSpinBox(minimum=-50000, maximum=50000, value=5000)
    layout_aj_sph.addRow('coordonnées xmax:', xmax)
    layout_aj_sph.addRow(result_label)

    xmin = QSpinBox(minimum=-50000, maximum=50000, value=-5000)
    layout_aj_sph.addRow('coordonnées xmin:', xmin)
    layout_aj_sph.addRow(result_label)

    ymax = QSpinBox(minimum=-50000, maximum=50000, value=5000)
    layout_aj_sph.addRow('coordonnées ymax:', ymax)
    layout_aj_sph.addRow(result_label)

    ymin = QSpinBox(minimum=-50000, maximum=50000, value=-5000)
    layout_aj_sph.addRow('coordonnées ymin:', ymin)
    layout_aj_sph.addRow(result_label)

    zmax = QSpinBox(minimum=10, maximum=50000, value=10)
    layout_aj_sph.addRow('coordonnées zmax:', zmax)
    layout_aj_sph.addRow(result_label)

    zmin = QSpinBox(minimum=10, maximum=50000, value=10)
    layout_aj_sph.addRow('coordonnées zmin:', zmin)
    layout_aj_sph.addRow(result_label)


    xmin=xmin.value()
    xmax=xmax.value()
    ymin=ymin.value()
    ymax=ymax.value()
    zmin=zmin.value()
    zmax=zmax.value()
    if xmin>xmax:
        tmp=xmin
        xmin=xmax
        xmax=tmp
    if ymin>ymax:
        tmp=ymin
        ymin=ymax
        ymax=tmp
    if zmin>zmax:
        tmp=zmin
        zmin=zmax
        zmax=tmp
    
    def ajouter_spheres(boo: bool) -> None:
        for i in range(Controles.amount.value()):
            x=randint(Controles.xmin,Controles.xmax)
            y=randint(Controles.ymin,Controles.ymax)
            z=randint(Controles.zmin,Controles.zmax)
            var = gravilib.PyBaseSphere(x, y, z, randint(
                1, 100000000), randint(3000, 10000), randint(-400, 400), randint(-400, 400), randint(-3, 3), 10)
            Fenetre_principale.ajouter_sphere(var)
    
    """def ajouter_spheres(boo: bool) -> None:
        for i in range(Controles.amount.value()):
            xmin = (Controles.x.value()*10-2000)*10
            xmax = (Controles.x.value()*10+2000)*10
            ymin = (Controles.y.value()*10-2000)*10
            ymax = (Controles.y.value()*10+2000)*10
            var = gravilib.PyBaseSphere(randint(xmin, xmax)*10, randint(ymin, ymax)*10, 10, randint(
                1, 100000000), randint(3000, 10000), randint(-400, 400), randint(-400, 400), randint(-3, 3), 10)
            Fenetre_principale.ajouter_sphere(var)"""

    bouton_val_aj: QAbstractButton = QPushButton("Ajouter les sphères")
    layout_aj_sph.addWidget(bouton_val_aj)
    bouton_val_aj.clicked.connect(ajouter_spheres)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Controles")
        # layout of controles widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        boutton1: QAbstractButton = QPushButton("Ajout direct")
        boutton1.clicked.connect(Controles.ajouter_spheres)
        self.layout.addWidget(boutton1)

        self.boutt_show_aj_sph: QAbstractButton = QPushButton(
            "Ajouter des sphère")
        self.layout.addWidget(self.boutt_show_aj_sph)
        self.boutt_show_aj_sph.clicked.connect(self.fenetre_ajoute.show)


controles_graphiques: QWidget = Controles()
Fenetre_principale: QWidget = Main_window()


try:
    # Pour faire en sorte que la fenêtre prenne tout l'écran
    Fenetre_principale.showMaximized()
except:
    print("votre gestionnaire de fenetre est peu flexible")
    # Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même
    Fenetre_principale.show()
