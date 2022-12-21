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

    def fermeture(self):
        menu.close()

        


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        boutton = QPushButton("test")
        layout.addWidget(boutton)



app = QApplication(sys.argv)

Fenetre_principale = Main_window()
menu = Menu()

try:
    Fenetre_principale.showMaximized() #Pour faire en sorte que la fenêtre prenne tout l'écran 
except:
    Fenetre_principale.show() #Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même