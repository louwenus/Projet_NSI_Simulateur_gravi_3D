#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8

from . import settings
import sys
from sys import stderr
try:
    #import PySide6
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
except ModuleNotFoundError as e:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails",file=stderr)
    raise e
from . import gravilib
from .affichage3D import SphereItem,Renderer3D

import os

class Main_window(QWidget):
    """Définit la fenettre principale du programme, a partir d'un QWidget
    """
    def __init__(self) -> None:
        super().__init__()
        self.affichage_controles: bool = True

        self.setWindowTitle("Affichage")

        self.layout: QLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addSpacing(10)

        #creation des actions utiliseables dans les menus
        self.attach_detachAction: QAction = QAction("&Détacher les contrôles", self)
        self.attach_detachAction.triggered.connect(self.attach_detach_controles)

        self.licenseAction: QAction = QAction("&Lire la license", self)
        self.licenseAction.triggered.connect(self.affich_licence)

        #création des menus
        self.menuBar:QWidget = QMenuBar(self)
        
        self.affichageMenu:QMenu= QMenu("&Affichage",self.menuBar)
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.attach_detachAction)

        self.helpMenu:QMenu= QMenu("&Help",self.menuBar)
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(self.licenseAction)

        #fenettre détacheable de controle
        self.affichage_controles: bool = True
        self.controles=QWidget()
        self.contr_L=QVBoxLayout()
        self.contr_L.addWidget(controles_graphiques)
        self.controles.setLayout(self.contr_L)
        self.layout.addWidget(controles_graphiques)
        
        
        #widget de rendu3D
        self.widget_3D: Renderer3D=Renderer3D()
        self.layout.addWidget(self.widget_3D)
        
        #dimension affiché par la fennettre de rendu
        self.dimension=gravilib.PyBaseDimension()
        
        #a raffiner, mais est utilisé pour update la simulation toute les 10ms
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()
        if settings.get("logging")>=2:
            print("main windows initialized")


    def closeEvent(self, event) -> None: 
        # Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme
        app.exit(0)


    def attach_detach_controles(self) -> None:
        if self.affichage_controles :
            self.controles.hide()
            maincontroles.show()
            self.attach_detachAction.setText("&Attacher les contrôles")
            self.affichage_controles = False
            if settings.get("logging")>=2:
                print("controles déttachés")
        else :
            self.controles.show()
            maincontroles.hide()
            self.attach_detachAction.setText("&Détacher les contrôles")
            self.affichage_controles = True
            if settings.get("logging")>=2:
                print("controles attachés")




    def affich_licence(self) -> None:
        self.fenetre_license: QWidget = QScrollArea()
        self.fenetre_license.setWindowTitle("LICENSE")
        
        try:
            path: str=os.path.abspath(os.path.dirname(__file__))
            path=os.path.join(path, "LICENSCE_FR")
            with open(path) as file:
                self.licenseTextlabel:QWidget = QLabel(file.read())
        except:
            if settings.get("logging")>=1:
                print("The french licence file was not found at",path,file=stderr)
            self.licenseTextlabel: QWidget = QLabel("Ficher manquant ou chemin cassé.\n\nRendez vous sur :\nhttps://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D/blob/main/LICENSCE_FR")

        self.fenetre_license.setWidget(self.licenseTextlabel)
        self.fenetre_license.show()

    
    def ajouter_sphere(self,sph:gravilib.PyBaseSphere) -> None:
        self.dimension.add_sphere(sph)
        for rendu in sph.get_render_items():
            self.widget_3D.add_to_display(rendu)
    
    def update_simulation(self) -> None:
        self.dimension.gravite_all(0.1)
        self.dimension.move_all(0.1)
        self.dimension.gerer_colision()
        self.widget_3D.update_graph()
        sphere : gravilib.PyBaseSphere
        for sphere in self.dimension.get_spheres():
            pass

    

class Controles(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Controles")
        #layout of controles widget
        self.layout: QLayout = QHBoxLayout()
        self.setLayout(self.layout)
        self.dimension=gravilib.PyBaseDimension()
        
        boutton1: QAbstractButton = QPushButton("controle1")
        self.layout.addWidget(boutton1)

        
        self.fenetre_ajoute: QWidget = QScrollArea()
        self.fenetre_ajoute.setWindowTitle("Ajoutez des sphères !")
        self.layout_aj_sph:QLayout=QVBoxLayout()
        self.fenetre_ajoute.setLayout(self.layout_aj_sph)
        
        self.boutt_show_aj_sph: QPushButton = QPushButton("Ajouter une sphère")
        self.layout.addWidget(self.boutt_show_aj_sph)
        self.boutt_show_aj_sph.clicked.connect(self.fenetre_ajoute.show)
        
        self.boutton4: QPushButton = QPushButton("Ajouter la sphère")
        self.boutton4.clicked.connect(self.ajouter_spheres)
        self.layout_aj_sph.addWidget(self.boutton4)

    def ajouter_spheres(self) -> None:
        var = gravilib.PyBaseSphere(0, 0, 0, 1000000, 150, 100, 0, 0)
        Fenetre_principale.ajouter_sphere(var)




app: QApplication = QApplication(sys.argv)
controles_graphiques: QWidget = Controles()
maincontroles=QWidget()
main_con_L=QVBoxLayout()
main_con_L.addWidget(controles_graphiques)
maincontroles.setLayout(main_con_L)
Fenetre_principale: QWidget = Main_window()


try:
    Fenetre_principale.showMaximized() #Pour faire en sorte que la fenêtre prenne tout l'écran 
except:
    print("votre gestionnaire de fenetre est chiant")
    Fenetre_principale.show() #Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même