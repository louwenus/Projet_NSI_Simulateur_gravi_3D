#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding = utf8

import sys
import os
from sys import stderr
from math import cos, pi, sin
# import des différentes librairies non-standard avec debug en cas de librairie manquante
try:
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from random import *
    
except ModuleNotFoundError as e:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails", file=stderr)
    raise e

from . import settings
from . import gravilib
from .affichage3D import Renderer3D 
from . import langue

if settings.get("logging") >= 3:
    from time import time #importation de la libraire time


app: QApplication = QApplication(sys.argv)

class Main_window(QWidget):
    """Cette class définit la fenètre principale du programme, à partir d'un QWidget."""

    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)
        self.affichage_controles: bool = True

        self.setWindowTitle(langue.get("title"))

        self.layout: QLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addSpacing(10)

        # Création des actions utiliseables dans les menus
        self.attach_detachAction: QAction = QAction(langue.get("menu.display.detach"), self)
        self.attach_detachAction.triggered.connect(self.attach_detach_controles)

        self.licenseAction: QAction = QAction(langue.get("menu.help.license"), self)
        self.licenseAction.triggered.connect(self.affich_licence)

        # Création des menus
        self.menuBar: QWidget = QMenuBar(self)
        self.menuBar.setFixedWidth(self.size().width())

        self.affichageMenu: QMenu = QMenu(langue.get("menu.display.title"), self.menuBar)
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.attach_detachAction)
        
        self.configMenu: QMenu = QMenu(langue.get("menu.settings.title"), self.menuBar)
        self.menuBar.addMenu(self.configMenu)#TODO : ajout du selecteur de langue

        self.helpMenu: QMenu = QMenu(langue.get("menu.help.title"), self.menuBar)
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(self.licenseAction)

        # Fenètre détacheable de controle
        self.affichage_controles: bool = True
        self.controles = Controles()
        self.layout.addWidget(self.controles)

        # Widget de rendu3D
        self.widget_3D: Renderer3D = Renderer3D(self.controles)
        self.layout.addWidget(self.widget_3D)

        # Dimension affichée par la fenètre de rendu
        self.ticktime:float=1/settings.get("simulation.fps")*settings.get("simulation.simspeed")
        self.dimension = gravilib.PyBaseDimension(self.widget_3D,self.ticktime)
        
        # A raffiner, mais est utilisé pour update la simulation à intervalles réguliers
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(1/settings.get("simulation.fps")*1000)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()
        if settings.get("logging") >= 2:
            print("main windows initialized")


    def closeEvent(self, event) -> None:
        """Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme
        """
        app.exit(0)
        
    def keyPressEvent(self, event):
        # Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme grace aux touches
        if event.key() == Qt.Key_Escape:
            app.exit(0)
    
    def attach_detach_controles(self) -> None: 
        """Permet d'afficher les controles dans une fenètre séparée de la principale."""
        if self.affichage_controles:
            self.controles.hide()
            controles_graphiques.show()
            self.attach_detachAction.setText(langue.get("menu.display.attach"))
            self.affichage_controles = False
            if settings.get("logging") >= 2:
                print("controles déttachés")
        else:
            self.controles.show()
            controles_graphiques.hide()
            self.attach_detachAction.setText(langue.get("menu.display.detach"))
            self.affichage_controles = True
            if settings.get("logging") >= 2:
                print("controles attachés")

    def affich_licence(self) -> None:
        """Cette fonction permet d'afficher la licence du projet"""
        self.fenetre_license: QWidget = QScrollArea()
        self.fenetre_license.setWindowTitle(langue.get("file.license"))
        try:
            path: str = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(path, langue.get("file.license"))
            with open(path, encoding="utf-8") as file:
                self.licenseTextlabel: QWidget = QLabel(file.read())
        except:
            if settings.get("logging") >= 1:
                print("The french licence file was not found at", path, file=stderr)
            self.licenseTextlabel: QWidget = QLabel(
                "Ficher manquant ou chemin cassé.\n\nRendez vous sur :\nhttps://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D/blob/main/LICENCE_FR")
        self.fenetre_license.setWidget(self.licenseTextlabel)
        self.fenetre_license.show()

    def ajouter_sphere(self, sph: gravilib.PyBaseSphere) -> None:
        """Permet d'ajouter une sphère.

        Args:
            sph (gravilib.PyBaseSphere): Sphère venant de gravilib.py
        """
        self.dimension.add_sphere(sph)
        for rendu in sph.get_render_items():
            self.widget_3D.add_to_display(rendu)
    
    if  settings.get("logging")>=3:
        def update_simulation(self) -> None:
            totalstart = time()
            start = time()
            print("starting update")
            self.dimension.gravite_all()
            print("grav time:", time()-start)
            start = time()
            self.dimension.move_all()
            print("move time:", time()-start)
            start = time()
            self.dimension.gerer_colision()
            print("coli time", time()-start)
            start = time()
            self.widget_3D.repaint()
            print("graph time:", time()-start)
            print("total:", time()-totalstart,"on",self.ticktime,"normaly")
    else:
        def update_simulation(self) -> None:
            self.dimension.gravite_all()
            self.dimension.move_all()
            self.dimension.gerer_colision()
            self.widget_3D.repaint()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Décale la caméra par rapport au milieu de la fenêtre.

        Args:
            event (QResizeEvent): évenement de resize dans le widget.
        """
        self.menuBar.setFixedWidth(self.size().width())


class Controles(QWidget):
    """Classe permettant de gérer et afficher les contrôles des sphères ainsi que leurs effets.

    Args:
        QWidget (class 'Shiboken.ObjectType'): permet l'utilisation de Widgets.
    """
    """Ce QWidget permet de gérer les différents contrôles."""
    fenetre_ajoute: QWidget = QScrollArea()
    fenetre_ajoute.setWindowTitle(langue.get("control.add_settings.title"))
    layout_aj_sph: QLayout = QGridLayout()
    fenetre_ajoute.setLayout(layout_aj_sph)

    amount = QSpinBox(minimum=0, maximum=10000, value=100)
    layout_aj_sph.addWidget(QLabel(langue.get("control.add_settings.nb")), 0,0)
    layout_aj_sph.addWidget(amount,0,1)

    xmean = QDoubleSpinBox(minimum=-500000, maximum=500000, value=0,decimals=0)
    xrand = QDoubleSpinBox(minimum=-500000, maximum=500000, value=2000,decimals=0)
    for i,widget in enumerate((QLabel(langue.get("control.add_settings.x")), xmean, QLabel('+-'),xrand)):
        layout_aj_sph.addWidget(widget,1,i)

    ymean = QDoubleSpinBox(minimum=-500000, maximum=500000, value=0,decimals=0)
    yrand = QDoubleSpinBox(minimum=-500000, maximum=500000, value=2000,decimals=0)
    for i,widget in enumerate((QLabel(langue.get("control.add_settings.y")), ymean, QLabel('+-'),yrand)):
        layout_aj_sph.addWidget(widget,2,i)
    
    zmean = QDoubleSpinBox(minimum=-500000, maximum=500000, value=0,decimals=0)
    zrand = QDoubleSpinBox(minimum=-500000, maximum=500000, value=2000,decimals=0)
    for i,widget in enumerate((QLabel(langue.get("control.add_settings.z")), zmean, QLabel('+-'),zrand)):
        layout_aj_sph.addWidget(widget,3,i)
    
    massemin = QDoubleSpinBox(minimum=1, maximum=float(10**17), value=10**3,decimals=0)
    massemax = QDoubleSpinBox(minimum=1,maximum=float(10**17),value=10**4,decimals=0)
    for i,widget in enumerate((QLabel(langue.get("control.add_settings.m")), massemin, QLabel("<?<"),massemax)):
        layout_aj_sph.addWidget(widget,4,i)
    rayonmin = QDoubleSpinBox(minimum=1,maximum=10**7,value=3*10**4,decimals=0)
    rayonmax = QDoubleSpinBox(minimum=1,maximum=10**7,value=4*10**4,decimals=0)
    for i,widget in enumerate((QLabel(langue.get("control.add_settings.r")), rayonmin, QLabel("<?<"),rayonmax)):
        layout_aj_sph.addWidget(widget,5,i)
    
    def ajouter_spheres(*_) -> None:
        """Permet d'ajouter un nombre définie de sphères dans la plage de coordonnées selectionné.

        Args:
            boo (int): le nombre de sphères à ajouter.
        """
        xmean=Controles.xmean.value()*200000
        xrand=Controles.xrand.value()*200000
        ymean=Controles.ymean.value()*200000
        yrand=Controles.yrand.value()*200000
        zmean=Controles.zmean.value()*200000
        zrand=Controles.zrand.value()*200000
        mmin=Controles.massemin.value()*100
        mmax=Controles.massemax.value()*100
        rmin=Controles.rayonmin.value()*100
        rmax=Controles.rayonmax.value()*100
        for _ in range(Controles.amount.value()):
            dist:float=random()**(1/3)
            teta=random()*2*pi
            phi=random()*2*pi
            x=xmean+xrand*dist*sin(teta)*cos(phi)
            y=ymean+yrand*dist*sin(teta)*sin(phi)
            z=zmean+zrand*dist*cos(teta)
            var = gravilib.PyBaseSphere(x, y, z, randint(mmin, mmax), randint(rmin, rmax), randint(-400, 400), randint(-400, 400), randint(-400, 400), randint(10,1000000))
            Fenetre_principale.ajouter_sphere(var)

    bouton_val_aj: QAbstractButton = QPushButton(langue.get("control.add_settings.valid"))
    layout_aj_sph.addWidget(bouton_val_aj)
    bouton_val_aj.clicked.connect(ajouter_spheres)

    def __init__(self) -> None:
        """Méthode constructeur, permet de créer les boutons cliquables d'ajout de sphères.
        """
        super().__init__()
        self.setWindowTitle("Controles")
        # layout des controles widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        boutton1: QAbstractButton = QPushButton(langue.get("control.simple_add.title"))
        boutton1.clicked.connect(Controles.ajouter_spheres)
        self.layout.addWidget(boutton1)

        self.boutt_show_aj_sph: QAbstractButton = QPushButton(langue.get("control.add_settings.title"))
        self.layout.addWidget(self.boutt_show_aj_sph)
        self.boutt_show_aj_sph.clicked.connect(self.fenetre_ajoute.show)


controles_graphiques: QWidget = Controles()

Fenetre_principale: QWidget = Main_window()
Fenetre_principale.showMaximized()