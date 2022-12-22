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
        self.setWindowTitle("Affichage")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.widget_menu = Menu()
        self.layout.addWidget(self.widget_menu)

        self.boutton_menu1 = QPushButton("Détacher le menu")
        self.layout.addWidget(self.boutton_menu1)

        self.boutton_menu2 = QPushButton("Attacher le menu")
        self.layout.addWidget(self.boutton_menu2)
        self.boutton_menu2.hide()
        
        self.boutton_menu1.clicked.connect(self.detach_menu)
        self.boutton_menu2.clicked.connect(self.attach_menu)
        
        self.creer_actions()
        self.creer_barre_menu()
        self.connecter_actions()
        


    def creer_barre_menu(self):
        self.menuBar = QMenuBar(self)
        self.layout.addWidget(self.menuBar)
        
        self.affichageMenu = QMenu("&Affichage", self)
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.detachAction)
        self.affichageMenu.addAction(self.attachAction)


        self.helpMenu = QMenu("&Help", self)
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(self.licenseAction)

    def creer_actions(self):
        self.detachAction = QAction("&Détacher les contrôles", self)
        self.attachAction = QAction("&Attacher les contrôles", self)

        self.licenseAction = QAction("&Lire la license", self)

    def connecter_actions(self):
        self.detachAction.triggered.connect(self.detach_menu)
        self.attachAction.triggered.connect(self.attach_menu)

    def hide_menu(self):
        self.widget_menu.hide()
        
    def show_menu(self):
        self.widget_menu.show()

    def detach_menu(self):
        menu.show()
        self.hide_menu()
        self.boutton_menu1.hide()
        self.boutton_menu2.show()

    def attach_menu(self):
        menu.hide()
        self.show_menu()
        self.boutton_menu2.hide()
        self.boutton_menu1.show()

    def closeEvent(self, event): # Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme
        app.exit(0)

        


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        boutton1 = QPushButton("menu1")
        layout.addWidget(boutton1)

        boutton2 = QPushButton("menu2")
        layout.addWidget(boutton2)

        boutton3 = QPushButton("menu3")
        layout.addWidget(boutton3)



app = QApplication(sys.argv)

Fenetre_principale = Main_window()
menu = Menu()

try:
    Fenetre_principale.showMaximized() #Pour faire en sorte que la fenêtre prenne tout l'écran 
except:
    Fenetre_principale.show() #Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même