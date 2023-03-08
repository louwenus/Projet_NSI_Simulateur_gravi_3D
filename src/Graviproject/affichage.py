#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8

print("Importation de affichage.py")


try:
    #import PySide6
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
except ModuleNotFoundError:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")
from . import gravilib
from . import affichage3D
import sys
import os

class Main_window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.affichage_controles: bool = True

        self.setWindowTitle("Affichage")

        self.layout: QLayout = QHBoxLayout()
        self.setLayout(self.layout)

        self.widget_controles: QWidget = Controles()
        
        
        self.creer_actions()
        self.creer_barre_menu()

        self.layout.addWidget(self.widget_controles)
        self.widget_3D: affichage3D.MainWidget=affichage3D.MainWidget()
        self.layout.addWidget(self.widget_3D)
        
        
        self.connecter_actions()
        
        self.dimension=gravilib.cppgravilib.CyBaseDimension()
        
        self.sph = []
        self.sph.append(gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(1,1,1,0,10,10,20,20)))
        self.sph.append(gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(0,0,0,0,10,-10,-10,-10)))

        self.dimension.add_sphere(self.sph[0].cy_sphere)
        self.dimension.add_sphere(self.sph[1].cy_sphere)
        
        
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()


    def creer_barre_menu(self) -> None:
        self.menuBar:QWidget = QMenuBar(self)
        self.layout.addWidget(self.menuBar)
        
        self.affichageMenu:QMenu = QMenu("&Affichage", self)
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.attach_detachAction)

        self.helpMenu: QMenu = QMenu("&Help", self)
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(self.licenseAction)

    def creer_actions(self) -> None:
        self.attach_detachAction: QAction = QAction("&Détacher les contrôles", self)

        self.licenseAction: QAction = QAction("&Lire la license", self)

    def connecter_actions(self) -> None:
        self.attach_detachAction.triggered.connect(self.attach_detach_controles)
        self.licenseAction.triggered.connect(self.affich_licence)




    def attach_detach_controles(self) -> None:
        if self.affichage_controles :
            controles_graphiques.show()
            self.widget_controles.hide()
            self.attach_detachAction.setText("&Attacher les contrôles")
            self.affichage_controles = False

        else :
            controles_graphiques.hide()
            self.widget_controles.show()
            self.attach_detachAction.setText("&Détacher les contrôles")
            self.affichage_controles = True




    def affich_licence(self) -> None:
        self.fenetre_license: QWidget = QScrollArea()
        self.fenetre_license.setWindowTitle("LICENSE")
        
        try:
            path: str=os.path.abspath(os.path.dirname(__file__))
            path=os.path.join(path, "LICENSE")
            with open(path) as file:
                self.licenseTextlabel:QWidget = QLabel(file.read())
        except:
            self.licenseTextlabel: QWidget = QLabel("Ficher manquant ou chemin cassé.\n\nRendez vous sur :\nhttps://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D/blob/main/src/Graviproject/LICENSE")

        self.fenetre_license.setWidget(self.licenseTextlabel)
        self.fenetre_license.show()

        
        
        
    def closeEvent(self, event) -> None: # Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme
        app.exit(0)

    
    def ajouter_sphere(self,sph:gravilib.PyBaseSphere) -> None:
        self.dimension.add_sphere(sph.cy_sphere)
    
    def update_simulation(self) -> None:
        self.dimension.gravite_all(0.01)
        self.dimension.move_all(0.01)
        self.widget_3D.update_graph()
        sphere : gravilib.PyBaseSphere
        for sphere in self.dimension.get_spheres():
            #print(sphere.cy_sphere.get_coord())
            print(sphere)


class Controles(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Controles")
        
        layout: QLayout = QHBoxLayout()
        self.setLayout(layout)
        
        boutton1: QAbstractButton = QPushButton("controle1")
        layout.addWidget(boutton1)

        boutton2: QAbstractButton = QPushButton("controle2")
        layout.addWidget(boutton2)

        boutton3: QAbstractButton = QPushButton("controle3")
        layout.addWidget(boutton3)



app: QApplication = QApplication(sys.argv)

Fenetre_principale: QWidget = Main_window()
controles_graphiques: QWidget = Controles()

try:
    Fenetre_principale.showMaximized() #Pour faire en sorte que la fenêtre prenne tout l'écran 
except:
    print("votre gestionnaire de fenetre est chiant")
    Fenetre_principale.show() #Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même