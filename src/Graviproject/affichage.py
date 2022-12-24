#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8

print("Importation de affichage.py")


try:
    import PySide6
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
except ModuleNotFoundError:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")

import sys


class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.affichage_controles = True

        self.setWindowTitle("Affichage")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.widget_controles = Controles()
        
        self.creer_actions()
        self.creer_barre_menu()

        self.layout.addWidget(self.widget_controles)
        
        self.connecter_actions()




    def creer_barre_menu(self):
        self.menuBar = QMenuBar(self)
        self.layout.addWidget(self.menuBar)
        
        self.affichageMenu = QMenu("&Affichage", self)
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.attach_detachAction)

        self.helpMenu = QMenu("&Help", self)
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(self.licenseAction)

    def creer_actions(self):
        self.attach_detachAction = QAction("&Détacher les contrôles", self)

        self.licenseAction = QAction("&Lire la license", self)

    def connecter_actions(self):
        self.attach_detachAction.triggered.connect(self.attach_detach_controles)
        self.licenseAction.triggered.connect(self.affich_licence)




    def attach_detach_controles(self):
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




    def affich_licence(self):
        self.fenetre_license = QScrollArea()
        self.fenetre_license.setWindowTitle("LICENSE")
        
        try:
            with open("LICENSE") as file:
                self.licenseTextlabel = QLabel(file.read())

        except:
            self.licenseTextlabel = QLabel("arrg")

        self.fenetre_license.setWidget(self.licenseTextlabel)
        self.fenetre_license.show()

        
        
        
        



    def closeEvent(self, event): # Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme
        app.exit(0)

        


class Controles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controles")
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        boutton1 = QPushButton("controle1")
        layout.addWidget(boutton1)

        boutton2 = QPushButton("controle2")
        layout.addWidget(boutton2)

        boutton3 = QPushButton("controle3")
        layout.addWidget(boutton3)



app = QApplication(sys.argv)

Fenetre_principale = Main_window()
controles_graphiques = Controles()

try:
    Fenetre_principale.showMaximized() #Pour faire en sorte que la fenêtre prenne tout l'écran 
except:
    Fenetre_principale.show() #Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même