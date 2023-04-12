#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding = utf8


from . import settings #Importation du module settings du répertoire courant
#as logging is used realy often, put it in a var to decrease acess time
logging:int = settings.get("logging")
import sys #Importation de la librairie sys
from sys import stderr #Importation du module stderr de la librairie sys
try:
    # importation de PySide6
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from random import *
    
except ModuleNotFoundError as e:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails", file=stderr)
    raise e

from . import gravilib #Importation du module gravilib du répertoire courant
from .affichage3D import SphereItem, Renderer3D #Importation des class SphereItem, Renderer3D du module affichage3D dans le répertoire courant

import os #Importation de la librairie os

from time import time #importation de la libraire time

app: QApplication = QApplication(sys.argv)


class Main_window(QWidget):
    """Cette class définit la fenètre principale du programme, à partir d'un QWidget."""

    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)
        self.affichage_controles: bool = True

        self.setWindowTitle("Affichage")

        self.layout: QLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addSpacing(10)

        # Création des actions utiliseables dans les menus
        self.attach_detachAction: QAction = QAction(
            "&Détacher les contrôles", self)
        self.attach_detachAction.triggered.connect(
            self.attach_detach_controles)

        self.licenseAction: QAction = QAction("&Lire la licence", self)
        self.licenseAction.triggered.connect(self.affich_licence)

        # Création des menus
        self.menuBar: QWidget = QMenuBar(self)
        self.menuBar.setFixedWidth(self.size().width())

        self.affichageMenu: QMenu = QMenu("&Affichage", self.menuBar)
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.attach_detachAction)

        self.helpMenu: QMenu = QMenu("&Help", self.menuBar)
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
        self.dimension = gravilib.PyBaseDimension(self.widget_3D)
        
        # A raffiner, mais est utilisé pour update la simulation à intervalles réguliers
        self.ticktime:float=1/settings.get("simulation.fps")
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(self.ticktime*1000)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()
        if logging >= 2:
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
            self.attach_detachAction.setText("&Attacher les contrôles")
            self.affichage_controles = False
            if logging >= 2:
                print("controles déttachés")
        else:
            self.controles.show()
            controles_graphiques.hide()
            self.attach_detachAction.setText("&Détacher les contrôles")
            self.affichage_controles = True
            if logging >= 2:
                print("controles attachés")

    def affich_licence(self) -> None:
        """Cette fonction permet d'afficher la licence du projet"""
        self.fenetre_license: QWidget = QScrollArea()
        self.fenetre_license.setWindowTitle("LICENSE")
        try:
            path: str = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(path, "LICENSCE_FR")
            with open(path) as file:
                self.licenseTextlabel: QWidget = QLabel(file.read())
        except:
            if logging >= 1:
                print("The french licence file was not found at", path, file=stderr)
            self.licenseTextlabel: QWidget = QLabel(
                "Ficher manquant ou chemin cassé.\n\nRendez vous sur :\nhttps://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D/blob/main/LICENSCE_FR")
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
    if  logging>=3:
        def update_simulation(self) -> None:
            totalstart = time()
            start = time()
            print("starting update")
            self.dimension.gravite_all(self.ticktime)
            print("grav time:", time()-start)
            start = time()
            self.dimension.move_all(self.ticktime)
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
            self.dimension.gravite_all(self.ticktime)
            self.dimension.move_all(self.ticktime)
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
    fenetre_ajoute.setWindowTitle("Ajoutez des sphères !")
    layout_aj_sph: QLayout = QFormLayout()
    fenetre_ajoute.setLayout(layout_aj_sph)

    amount = QSpinBox(minimum=0, maximum=10000, value=100)
    result_label = QLabel('')
    layout_aj_sph.addRow('nb sphères:', amount)
    layout_aj_sph.addRow(result_label)

    xmax = QSpinBox(minimum=-500000, maximum=500000, value=2000)
    layout_aj_sph.addRow('coordonnées xmax:', xmax)
    layout_aj_sph.addRow(result_label)

    xmin = QSpinBox(minimum=-500000, maximum=500000, value=-2000)
    layout_aj_sph.addRow('coordonnées xmin:', xmin)
    layout_aj_sph.addRow(result_label)

    ymax = QSpinBox(minimum=-500000, maximum=500000, value=2000)
    layout_aj_sph.addRow('coordonnées ymax:', ymax)
    layout_aj_sph.addRow(result_label)

    ymin = QSpinBox(minimum=-500000, maximum=500000, value=-2000)
    layout_aj_sph.addRow('coordonnées ymin:', ymin)
    layout_aj_sph.addRow(result_label)

    zmax = QSpinBox(minimum=0, maximum=500000, value=1)
    layout_aj_sph.addRow('coordonnées zmax:', zmax)
    layout_aj_sph.addRow(result_label)

    zmin = QSpinBox(minimum=0, maximum=500000, value=1)
    layout_aj_sph.addRow('coordonnées zmin:', zmin)
    layout_aj_sph.addRow(result_label)
    
    #Valeurs multipliées par le nombre de balles à changer pour le projet final
    def ajouter_spheres(boo: bool) -> None:
        """Permet d'ajouter un nombre définie de sphères dans la plage de coordonnées selectionné.

        Args:
            boo (int): le nombre de sphères à ajouter.
        """
        xmin=Controles.xmin.value()*100
        xmax=Controles.xmax.value()*100
        ymin=Controles.ymin.value()*100
        ymax=Controles.ymax.value()*100
        zmin=Controles.zmin.value()*20
        zmax=Controles.zmax.value()*20
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
        for _ in range(Controles.amount.value()):
            x=randint(xmin,xmax)*Controles.amount.value()
            y=randint(ymin,ymax)*Controles.amount.value()
            z=randint(zmin,zmax)*Controles.amount.value()
            var = gravilib.PyBaseSphere(x, y, z, randint(1000, 1000000000), randint(30000, 400000), randint(-4000, 4000), randint(-4000, 4000), randint(-30, 30), randint(1,15))
            Fenetre_principale.ajouter_sphere(var)

    bouton_val_aj: QAbstractButton = QPushButton("Ajouter les sphères")
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

        boutton1: QAbstractButton = QPushButton("Ajout direct")
        boutton1.clicked.connect(Controles.ajouter_spheres)
        self.layout.addWidget(boutton1)

        self.boutt_show_aj_sph: QAbstractButton = QPushButton("Ajouter des sphères")
        self.layout.addWidget(self.boutt_show_aj_sph)
        self.boutt_show_aj_sph.clicked.connect(self.fenetre_ajoute.show)


controles_graphiques: QWidget = Controles()
Fenetre_principale: QWidget = Main_window()



try:
    # Afin de la fenètre prenne tout l'écran
    Fenetre_principale.showMaximized()
    
except:
    print("Votre gestionnaire de fenetre est peu flexible")
    # Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même
    Fenetre_principale.show()
